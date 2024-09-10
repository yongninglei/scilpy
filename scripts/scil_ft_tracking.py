#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Local streamline tractography based on the architecture of
scil_tracking_local_dev.py, adapted for fibertube tracking.

Void of the concept of grid, voxels and resolution. Instead, the tracking
algorithm is executed directly on fibertubes (Virtual representation of
axons). To simulate a lower resolution, a blur_radius parameter forming a
"tracking sphere" is introduced. At each step, a random direction will be
picked from the fibertube segments intersecting with the tracking sphere.

Algorithm type is inherently probabilistic with a distribution weighted by the
volume of intersection between each fibertube segment and the tracking sphere.

The tracking direction is chosen in the aperture cone defined by the
previous tracking direction and the angular constraint.

Seeding is done within the first segment of each fibertube.
"""

import os
import json
import time
import argparse
import logging
import numpy as np
import nibabel as nib
import dipy.core.geometry as gm

from scilpy.tracking.seed import FibertubeSeedGenerator
from scilpy.tracking.propagator import FibertubePropagator
from scilpy.image.volume_space_management import FibertubeDataVolume
from dipy.io.stateful_tractogram import StatefulTractogram, Space, Origin
from dipy.io.streamline import load_tractogram, save_tractogram
from scilpy.tracking.tracker import Tracker
from scilpy.image.volume_space_management import DataVolume
from scilpy.io.utils import (assert_inputs_exist,
                             assert_outputs_exist,
                             add_processes_arg,
                             add_verbose_arg,
                             add_json_args,
                             add_overwrite_arg)


def _build_arg_parser():
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__)

    p.add_argument('in_fibertubes',
                   help='Path to the tractogram file containing the \n'
                        'fibertubes with their respective diameter saved \n'
                        'as data_per_streamline (must be .trk). \n'
                        'The fibertubes must be void of any collision \n'
                        '(see scil_filter_intersections.py). \n')

    p.add_argument('out_tractogram',
                   help='Tractogram output file (must be .trk or .tck).')

    p.add_argument('step_size', type=float,
                   help='Step size of the tracking algorithm, in mm. \n'
                   'A step_size within [0.001, 0.5] is recommended.')

    p.add_argument('blur_radius', type=float,
                   help='Radius of the spherical region from which the \n'
                   'algorithm will determine the next direction. \n'
                   'A blur_radius within [0.001, 0.5] is recommended.')

    track_g = p.add_argument_group('Tracking options')
    track_g.add_argument(
        '--min_length', type=float, default=10.,
        metavar='m',
        help='Minimum length of a streamline in mm. '
        '[%(default)s]')
    track_g.add_argument(
        '--max_length', type=float, default=300.,
        metavar='M',
        help='Maximum length of a streamline in mm. '
        '[%(default)s]')
    track_g.add_argument(
        '--theta', type=float, default=60.,
        help='Maximum angle between 2 steps. If the angle is '
             'too big, streamline is \nstopped and the '
             'following point is NOT included.\n'
             '[%(default)s]')
    track_g.add_argument(
        '--rk_order', metavar="K", type=int, default=1,
        choices=[1, 2, 4],
        help="The order of the Runge-Kutta integration used \n"
             'for the step function. \n'
             'For more information, refer to the note in the \n'
             'script description. [%(default)s]')
    track_g.add_argument(
        '--max_invalid_nb_points', metavar='MAX', type=int,
        default=0,
        help='Maximum number of steps without valid \n'
             'direction, \nex: No fibertube intersecting the \n'
             'tracking sphere or max angle is reached.\n'
             'Default: 0, i.e. do not add points following '
             'an invalid direction.')
    track_g.add_argument(
        '--forward_only', action='store_true',
        help='If set, tracks in one direction only (forward) \n'
             'given the \ninitial seed.')
    track_g.add_argument(
        '--keep_last_out_point', action='store_true',
        help='If set, keep the last point (once out of the \n'
             'tracking mask) of the streamline. Default: discard \n'
             'them. This is the default in Dipy too. \n'
             'Note that points obtained after an invalid direction \n'
             '(based on the propagator\'s definition of invalid) \n'
             'are never added.')

    seed_group = p.add_argument_group(
        'Seeding options',
        'When no option is provided, uses --nb_seeds_per_fiber 5.')
    seed_group.add_argument(
        '--nb_seeds_per_fiber', type=int, default=5,
        help='The number of seeds planted in the first segment \n'
             'of each fiber. The total amount of streamlines will \n'
             'be [nb_seeds_per_fiber] * [nb_fibers]. [%(default)s]')
    seed_group.add_argument(
        '--nb_fibers', type=int,
        help='If set, the script will only track a specified \n'
             'amount of fibers. Otherwise, the entire tractogram \n'
             'will be tracked. The total amount of streamlines \n'
             'will be [nb_seeds_per_fiber] * [nb_fibers].')

    rand_g = p.add_argument_group('Random options')
    rand_g.add_argument(
        '--rng_seed', type=int, default=0,
        help='If set, all random values will be generated \n'
        'using the specified seed. [%(default)s]')
    rand_g.add_argument(
        '--skip', type=int, default=0,
        help="Skip the first N seeds. \n"
             "Useful if you want to create new streamlines to "
             "add to \na previously created tractogram with a "
             "fixed --rng_seed.\nEx: If tractogram_1 was created "
             "with -nt 1,000,000, \nyou can create tractogram_2 "
             "with \n--skip 1,000,000.")

    out_g = p.add_argument_group('Output options')
    out_g.add_argument(
        '--do_not_save_seeds', action='store_true',
        help='If set, the seeds used for tracking will not be saved \n'
             'as data_per_streamline in [out_tractogram]. Seeds are needed \n'
             'if you wish to compute fibertube reconstruction metrics later.')
    out_g.add_argument(
        '--out_config', default=None, type=str,
        help='If set, the parameter configuration used for tracking will \n'
        'be saved at the specified location (must be .txt). If not given, \n'
        'the config will be printed in the console.')

    add_overwrite_arg(out_g)
    add_processes_arg(p)
    add_verbose_arg(p)
    add_json_args(p)

    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('numba').setLevel(logging.WARNING)

    if not nib.streamlines.is_supported(args.in_fibertubes):
        parser.error('Invalid input streamline file format (must be trk ' +
                     'or tck): {0}'.format(args.in_fibertubes))

    if not nib.streamlines.is_supported(args.out_tractogram):
        parser.error('Invalid output streamline file format (must be trk ' +
                     'or tck): {0}'.format(args.out_tractogram))

    out_tractogram_no_ext, ext = os.path.splitext(args.out_tractogram)

    outputs = [args.out_tractogram]
    if not args.do_not_save_seeds:
        outputs.append(out_tractogram_no_ext + '_seeds' + ext)

    assert_inputs_exist(parser, [args.in_fibertubes])
    assert_outputs_exist(parser, args, outputs, [args.out_config])

    theta = gm.math.radians(args.theta)

    max_nbr_pts = int(args.max_length / args.step_size)
    min_nbr_pts = max(int(args.min_length / args.step_size), 1)

    our_space = Space.VOXMM
    our_origin = Origin('center')

    logging.debug('Loading tractogram & diameters')
    in_sft = load_tractogram(args.in_fibertubes, 'same', our_space, our_origin)
    centerlines = list(in_sft.get_streamlines_copy())
    diameters = np.reshape(in_sft.data_per_streamline['diameters'],
                           len(centerlines))

    logging.debug("Instantiating datavolumes")
    fake_mask_data = np.ones(in_sft.dimensions)
    fake_mask = DataVolume(fake_mask_data, in_sft.voxel_sizes, 'nearest')
    datavolume = FibertubeDataVolume(centerlines, diameters, in_sft,
                                     args.blur_radius,
                                     np.random.default_rng(args.rng_seed))

    logging.debug("Instantiating seed generator")
    seed_generator = FibertubeSeedGenerator(centerlines, diameters,
                                            args.nb_seeds_per_fiber)

    logging.debug("Instantiating propagator")
    propagator = FibertubePropagator(datavolume, args.step_size,
                                     args.rk_order, theta, our_space,
                                     our_origin)

    logging.debug("Instantiating tracker")
    if args.nb_fibers:
        nbr_seeds = args.nb_seeds_per_fiber * args.nb_fibers
    else:
        nbr_seeds = args.nb_seeds_per_fiber * len(centerlines)

    tracker = Tracker(propagator, fake_mask, seed_generator, nbr_seeds,
                      min_nbr_pts, max_nbr_pts,
                      args.max_invalid_nb_points, 0,
                      args.nbr_processes, not args.do_not_save_seeds, 'r+',
                      rng_seed=args.rng_seed,
                      track_forward_only=args.forward_only,
                      skip=args.skip,
                      verbose=args.verbose,
                      append_last_point=args.keep_last_out_point)

    start_time = time.time()
    logging.debug("Tracking...")
    streamlines, seeds = tracker.track()
    str_time = "%.2f" % (time.time() - start_time)
    logging.debug('Finished tracking in: ' + str_time + ' seconds')

    out_sft = StatefulTractogram.from_sft(streamlines, in_sft)
    if not args.do_not_save_seeds:
        out_sft.data_per_streamline['seeds'] = seeds
    save_tractogram(out_sft, args.out_tractogram)

    if args.out_config:
        config = {
            'step_size': args.step_size,
            'blur_radius': args.blur_radius,
            'nb_fibers': args.nb_fibers,
            'nb_seeds_per_fiber': args.nb_seeds_per_fiber
        }
        with open(args.out_config, 'w') as outfile:
            json.dump(config, outfile,
                      indent=args.indent, sort_keys=args.sort_keys)
    else:
        print('Config:\n',
              json.dumps(config, indent=args.indent, sort_keys=args.sort_keys))


if __name__ == "__main__":
    main()
