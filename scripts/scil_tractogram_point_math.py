#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performs an operation on data per point from input streamlines.

Two modes of operation are supported: data per streamline (dps) and data per
point (dpp).

In dps mode, the operation is performed across all dimensions of the data
resulting in a single value per streamline.

In dpp mode the operation is performed on each point separately, resulting in
a single value per point.

If endpoints_only and dpp mode is set operation will only
be calculated at the streamline endpoints the rest of the
values along the streamline will be NaN

If endpoints_only and dps mode is set operation will be calculated
across the data at the endpoints and stored as a
single value per streamline.

Endpoint only operation:
correlation: correlation calculated between arrays extracted from
streamline endpoints (data must be multivalued per point) and dps
mode must be set.
"""

import argparse
import logging

from dipy.io.streamline import save_tractogram, StatefulTractogram

from scilpy.io.streamlines import load_tractogram_with_reference
from scilpy.io.utils import (add_bbox_arg,
                             add_overwrite_arg,
                             add_reference_arg,
                             add_verbose_arg,
                             assert_inputs_exist,
                             assert_outputs_exist)
from scilpy.tractograms.streamline_operations import (
        perform_pairwise_streamline_operation_on_endpoints,
        perform_streamline_operation_per_point,
        perform_operation_per_streamline)


def _build_arg_parser():
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__)

    p.add_argument('operation', metavar='OPERATION',
                   choices=['mean', 'sum', 'min',
                            'max', 'correlation'],
                   help='The type of operation to be performed on the '
                        'streamlines. Must\nbe one of the following: '
                        '%(choices)s.')
    p.add_argument('dpp_or_dps', metavar='DPP_OR_DPS',
                   choices=['dpp', 'dps'],
                   help='Set to dps if the operation is to be performed '
                   'across all dimensions resulting in a single value per '
                   'streamline. Set to dpp if the operation is to be '
                   'performed on each point separately resulting in a single '
                   'value per point.')
    p.add_argument('in_tractogram', metavar='INPUT_FILE',
                   help='Input tractogram containing streamlines and '
                        'metadata.')
    p.add_argument('--in_dpp_name',  nargs='+', action='append',
                   required=True,
                   help='Name or list of names of the data_per_point for '
                        'operation to be performed on. If more than one dpp '
                        'is selected, the same operation will be applied '
                        'separately to each one.')
    p.add_argument('--out_name', nargs='+', action='append',
                   required=True,
                   help='Name of the resulting data_per_point or '
                   'data_per_streamline to be saved in the output '
                   'tractogram. If more than one --in_dpp_name was used, '
                   'enter the same number of --out_name values.')
    p.add_argument('out_tractogram', metavar='OUTPUT_FILE',
                   help='The file where the remaining streamlines '
                        'are saved.')

    p.add_argument('--endpoints_only', action='store_true', default=False,
                   help='If set, will only perform operation on endpoints \n'
                   'If not set, will perform operation on all streamline \n'
                   'points.')

    add_reference_arg(p)
    add_verbose_arg(p)
    add_overwrite_arg(p)
    add_bbox_arg(p)

    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    assert_inputs_exist(parser, args.in_tractogram)
    assert_outputs_exist(parser, args, args.out_tractogram)

    # Load the input files.
    logging.info("Loading file {}".format(args.in_tractogram))
    sft = load_tractogram_with_reference(parser, args, args.in_tractogram)

    if len(sft.streamlines) == 0:
        logging.info("Input tractogram contains no streamlines. Exiting.")
        return

    if len(args.in_dpp_name[0]) != len(args.out_name[0]):
        parser.error('The number of in_dpp_names and out_names must be '
                     'the same.')

    # Check to see if there are duplicates in the out_names
    if len(args.out_name[0]) != len(set(args.out_name[0])):
        parser.error('The output names (out_names) must be unique.')

    # Input name checks
    for in_dpp_name in args.in_dpp_name[0]:
        # Check to see if the data per point exists.
        if in_dpp_name not in sft.data_per_point:
            logging.info('Data per point {} not found in input tractogram.'
                         .format(in_dpp_name))
            return

        data_shape = sft.data_per_point[in_dpp_name][0].shape
        if args.operation == 'correlation' and len(data_shape) == 1:
            logging.info('Correlation operation requires multivalued data per '
                         'point. Exiting.')
            return

        if args.operation == 'correlation' and args.dpp_or_dps == 'dpp':
            logging.info('Correlation operation requires dps mode. Exiting.')
            return

    data_per_point = {}
    data_per_streamline = {}
    for in_dpp_name, out_name in zip(args.in_dpp_name[0],
                                     args.out_name[0]):


        # Perform the requested operation.
        if args.operation == 'correlation':
            logging.info('Performing {} across endpoint data and saving as '
                         'new dpp {}'.format(
                args.operation, out_name))
            new_dps = perform_pairwise_streamline_operation_on_endpoints(
                args.operation, sft, in_dpp_name)

            data_per_streamline[out_name] = new_dps
        elif args.dpp_or_dps == 'dpp':
            # Results in new data per point
            logging.info(
                'Performing {} on data from each streamine point '
                'and saving as new dpp {}'.format(
                    args.operation, out_name))
            new_dpp = perform_streamline_operation_per_point(
                args.operation, sft, in_dpp_name, args.endpoints_only)
            data_per_point[out_name] = new_dpp
        elif args.dpp_or_dps == 'dps':
            # Results in new data per streamline
            logging.info(
                'Performing {} across each streamline and saving resulting '
                'data per streamline {}'.format(args.operation, out_name))
            new_data_per_streamline = perform_operation_per_streamline(
                args.operation, sft, in_dpp_name, args.endpoints_only)
            data_per_streamline[out_name] = new_data_per_streamline

    new_sft = StatefulTractogram(sft.streamlines,
                                 sft.space_attributes,
                                 sft.space, sft.origin,
                                 data_per_point=data_per_point,
                                 data_per_streamline=data_per_streamline)

    # Save the new streamlines (and metadata)
    logging.info('Saving {} streamlines to {}.'.format(len(new_sft),
                                                       args.out_tractogram))
    save_tractogram(new_sft, args.out_tractogram,
                    bbox_valid_check=args.bbox_check)


if __name__ == "__main__":
    main()
