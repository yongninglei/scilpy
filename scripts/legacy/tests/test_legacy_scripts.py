#!/usr/bin/env python3
# -*- coding: utf-8 -*-

legacy_scripts_list_tag_1_6_0 = [
    "scil_add_tracking_mask_to_pft_maps.py",
    "scil_analyse_lesions_load.py",
    "scil_apply_bias_field_on_dwi.py",
    "scil_apply_transform_to_bvecs.py",
    "scil_apply_transform_to_hdf5.py",
    "scil_apply_transform_to_image.py",
    "scil_apply_transform_to_surface.py",
    "scil_apply_transform_to_tractogram.py",
    "scil_assign_custom_color_to_tractogram.py",
    "scil_assign_uniform_color_to_tractograms.py",
    "scil_clean_qbx_clusters.py",
    "scil_combine_labels.py",
    "scil_compare_connectivity.py",
    "scil_compress_streamlines.py",
    "scil_compute_asym_odf_metrics.py",
    "scil_compute_bundle_mean_std_per_point.py",
    "scil_compute_bundle_mean_std.py",
    "scil_compute_bundle_volume_per_label.py",
    "scil_compute_bundle_volume.py",
    "scil_compute_bundle_voxel_label_map.py",
    "scil_compute_centroid.py",
    "scil_compute_connectivity.py",
    "scil_compute_divide.py",
    "scil_compute_dti_metrics.py",
    "scil_compute_endpoints_map.py",
    "scil_compute_fodf_max_in_ventricles.py",
    "scil_compute_fodf_metrics.py",
    "scil_compute_freewater.py",
    "scil_compute_hdf5_average_density_map.py",
    "scil_compute_ihMT_maps.py",
    "scil_compute_kurtosis_metrics.py",
    "scil_compute_lobe_specific_fodf_metrics.py",
    "scil_compute_local_tracking_dev.py",
    "scil_compute_local_tracking.py",
    "scil_compute_maps_for_particle_filter_tracking.py",
    "scil_compute_mean_fixel_afd_from_bundles.py",
    "scil_compute_mean_fixel_afd_from_hdf5.py",
    "scil_compute_mean_fixel_lobe_metric_from_bundles.py",
    "scil_compute_mean_frf.py",
    "scil_compute_memsmt_fodf.py",
    "scil_compute_memsmt_frf.py",
    "scil_compute_metrics_stats_in_ROI.py",
    "scil_compute_msmt_fodf.py",
    "scil_compute_msmt_frf.py",
    "scil_compute_MT_maps.py",
    "scil_compute_NODDI_priors.py",
    "scil_compute_NODDI.py",
    "scil_compute_pca.py",
    "scil_compute_pft.py",
    "scil_compute_powder_average.py",
    "scil_compute_qball_metrics.py",
    "scil_compute_qbx.py",
    "scil_compute_rish_from_sh.py",
    "scil_compute_seed_by_labels.py",
    "scil_compute_seed_density_map.py",
    "scil_compute_sf_from_sh.py",
    "scil_compute_sh_from_signal.py",
    "scil_compute_ssst_fodf.py",
    "scil_compute_ssst_frf.py",
    "scil_compute_streamlines_density_map.py",
    "scil_compute_streamlines_length_stats.py",
    "scil_compute_todi.py",
    "scil_concatenate_dwi.py",
    "scil_connectivity_math.py",
    "scil_convert_fdf.py",
    "scil_convert_gradients_fsl_to_mrtrix.py",
    "scil_convert_gradients_mrtrix_to_fsl.py",
    "scil_convert_json_to_xlsx.py",
    "scil_convert_rgb.py",
    "scil_convert_sh_basis.py",
    "scil_convert_surface.py",
    "scil_convert_tensors.py",
    "scil_convert_tractogram.py",
    "scil_count_non_zero_voxels.py",
    "scil_count_streamlines.py",
    "scil_crop_volume.py",
    "scil_cut_streamlines.py",
    "scil_decompose_connectivity.py",
    "scil_detect_dwi_volume_outliers.py",
    "scil_detect_streamlines_loops.py",
    "scil_dilate_labels.py",
    "scil_estimate_bundles_diameter.py",
    "scil_evaluate_bundles_binary_classification_measures.py",
    "scil_evaluate_bundles_individual_measures.py",
    "scil_evaluate_bundles_pairwise_agreement_measures.py",
    "scil_evaluate_connectivity_graph_measures.py",
    "scil_evaluate_connectivity_pairwise_agreement_measures.py",
    "scil_execute_angle_aware_bilateral_filtering.py",
    "scil_execute_asymmetric_filtering.py",
    "scil_extract_b0.py",
    "scil_extract_dwi_shell.py",
    "scil_extract_ushape.py",
    "scil_filter_connectivity.py",
    "scil_filter_streamlines_by_length.py",
    "scil_filter_streamlines_by_orientation.py",
    "scil_filter_tractogram_anatomically.py",
    "scil_filter_tractogram.py",
    "scil_fit_bingham_to_fodf.py",
    "scil_fix_dsi_studio_trk.py",
    "scil_flip_gradients.py",
    "scil_flip_streamlines.py",
    "scil_flip_surface.py",
    "scil_flip_volume.py",
    "scil_generate_gradient_sampling.py",
    "scil_generate_priors_from_bundle.py",
    "scil_get_version.py",
    "scil_group_comparison.py",
    "scil_harmonize_json.py",
    "scil_image_math.py",
    "scil_merge_json.py",
    "scil_merge_sh.py",
    "scil_normalize_connectivity.py",
    "scil_outlier_rejection.py",
    "scil_perform_majority_vote.py",
    "scil_plot_mean_std_per_point.py",
    "scil_prepare_eddy_command.py",
    "scil_prepare_topup_command.py",
    "scil_print_connectivity_filenames.py",
    "scil_print_header.py",
    "scil_project_streamlines_to_map.py",
    "scil_recognize_multi_bundles.py",
    "scil_recognize_single_bundle.py",
    "scil_register_tractogram.py",
    "scil_remove_invalid_streamlines.py",
    "scil_remove_labels.py",
    "scil_remove_outliers_ransac.py",
    "scil_remove_similar_streamlines.py",
    "scil_reorder_connectivity.py",
    "scil_reorder_dwi_philips.py",
    "scil_resample_bvals.py",
    "scil_resample_streamlines.py",
    "scil_resample_tractogram.py",
    "scil_resample_volume.py",
    "scil_reshape_to_reference.py",
    "scil_run_commit.py",
    "scil_run_nlmeans.py",
    "scil_save_connections_from_hdf5.py",
    "scil_score_bundles.py",
    "scil_score_tractogram.py",
    "scil_screenshot_bundle.py",
    "scil_screenshot_dti.py",
    "scil_screenshot_volume_mosaic_overlap.py",
    "scil_screenshot_volume.py",
    "scil_search_keywords.py",
    "scil_set_response_function.py",
    "scil_shuffle_streamlines.py",
    "scil_smooth_streamlines.py",
    "scil_smooth_surface.py",
    "scil_snr_in_roi.py",
    "scil_split_image.py",
    "scil_split_tractogram.py",
    "scil_split_volume_by_ids.py",
    "scil_split_volume_by_labels.py",
    "scil_streamlines_math.py",
    "scil_swap_gradient_axis.py",
    "scil_tractogram_math.py",
    "scil_uniformize_streamlines_endpoints.py",
    "scil_validate_and_correct_bvecs.py",
    "scil_validate_and_correct_eddy_gradients.py",
    "scil_validate_bids.py",
    "scil_verify_space_attributes_compatibility.py",
    "scil_visualize_bingham_fit.py",
    "scil_visualize_bundles_mosaic.py",
    "scil_visualize_bundles.py",
    "scil_visualize_connectivity.py",
    "scil_visualize_fodf.py",
    "scil_visualize_gradients.py",
    "scil_visualize_histogram.py",
    "scil_visualize_scatterplot.py",
    "scil_visualize_seeds_3d.py",
    "scil_visualize_seeds.py"]


# test that all scripts available in scilpy 1.6.0 can be called
def test_help_option(script_runner):
    for script in legacy_scripts_list_tag_1_6_0:
        ret = script_runner.run('  ' + script, '--help')
        assert ret.success
