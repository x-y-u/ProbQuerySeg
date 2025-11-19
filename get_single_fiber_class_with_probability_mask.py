"""
    coding: utf-8
    Project: Fiber_Query
    File: get_single_fiber_class_with_probability_mask.py
    Author: xieyu
    Date: 2025/8/11 11:47
    IDE: PyCharm
"""
import os

import nibabel as nib
import numpy as np
from dipy.io.stateful_tractogram import StatefulTractogram
from dipy.io.streamline import save_tractogram

from tqdm import tqdm

from utils import get_bundle_names, get_single_fiber_class, read_lines_as_vox_indices, read_lines, get_end_points, \
    lines_RASMM_2_VOX_indices, read_combos_as_map


def main():
    # tck_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_tracts_tck/"

    tck_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    mask_base_path = "/media/UG3/xieyu/fiber_query/HCP/population_multi_mask_in_person/"
    end_points_mask_base_path = "/media/UG3/xieyu/fiber_query/HCP/population_end_points_multi_mask_in_person/"

    extended_aparc_base_path = "/media/UG3/xieyu/fiber_query/HCP/extended_aparc/"

    # out_base_path = "/media/UG3/xieyu/tractography_generate/HCP/recognize_results/"

    out_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    sample_names = os.listdir(tck_base_path)

    sample_names = ['622236']

    bundle_names = get_bundle_names()

    combos = read_combos_as_map("/media/UG3/xieyu/fiber_query/HCP/HCP_max_probability_pair/", bundle_names)

    for sample_name in tqdm(sample_names):
        print(sample_name)

        # org_file_path = os.path.join(dwi_base_path, sample_name, f"T1w/Diffusion/data.nii.gz")
        #
        # cur_tck_base_path = os.path.join(tck_base_path, sample_name, "tracts")

        cur_mask_path = os.path.join(mask_base_path, f"{sample_name}.nii.gz")
        cur_mask_nii = nib.load(cur_mask_path)
        cur_mask = cur_mask_nii.get_fdata()

        cur_end_points_mask_path = os.path.join(end_points_mask_base_path, f"{sample_name}.nii.gz")
        cur_end_points_mask_nii = nib.load(cur_end_points_mask_path)
        cur_end_points_mask = cur_end_points_mask_nii.get_fdata()

        # aparc_file_path = os.path.join(dwi_base_path, sample_name, f"T1w/aparc.a2009s+aseg.nii.gz")
        aparc_file_path = os.path.join(extended_aparc_base_path, f"{sample_name}.nii.gz")
        aparc_nii = nib.load(aparc_file_path)
        aparc_atlas = aparc_nii.get_fdata().astype(int)

        cur_whole_brain_path = os.path.join(tck_base_path, sample_name, "whole_brain.tck")

        cur_whole_brain_sft = read_lines(cur_whole_brain_path, cur_mask_path)
        cur_whole_brain_tck = cur_whole_brain_sft.streamlines

        cur_end_points = get_end_points(cur_whole_brain_tck)

        # cur_bundle_indices = lines_RASMM_2_VOX_indices(cur_whole_brain_tck, cur_mask_nii.affine)
        #
        # cur_end_points_indices = lines_RASMM_2_VOX_indices(cur_end_points, aparc_nii.affine)

        cur_bundle_indices = lines_RASMM_2_VOX_indices(cur_whole_brain_tck, cur_mask_nii.affine)

        cur_end_points_indices = lines_RASMM_2_VOX_indices(cur_end_points, cur_end_points_mask_nii.affine)

        cur_combo_points_indices = lines_RASMM_2_VOX_indices(cur_end_points, aparc_nii.affine)

        results = np.zeros((len(cur_whole_brain_tck), cur_mask.shape[3]))

        for index, line_indices, end_points, cur_combo_points in tqdm(
                zip(range(len(cur_whole_brain_tck)), cur_bundle_indices,
                    cur_end_points_indices, cur_combo_points_indices)):
            cur_class = get_single_fiber_class(line_indices, end_points, cur_combo_points, cur_mask,
                                               cur_end_points_mask, aparc_atlas,
                                               bundle_names, combos)
            if cur_class == -1 or cur_class == -2:
                pass
            else:
                results[index, cur_class] = 1

        np.save(os.path.join(tck_base_path, sample_name, "fiber_query_labels2.npy"), results)

        # for i, bundle_name in tqdm(enumerate(bundle_names)):
        #
        #     cur_out_base_path = os.path.join(out_base_path, sample_name, bundle_name)
        #     if not os.path.exists(cur_out_base_path):
        #         os.makedirs(cur_out_base_path)
        #
        #     cur_bundle_path = os.path.join(cur_tck_base_path, f"{bundle_name}.tck")
        #
        #     cur_sft = read_lines(cur_bundle_path, cur_mask_path)
        #     cur_bundle = cur_sft.streamlines
        #
        #     cur_end_points = get_end_points(cur_bundle)
        #
        #     cur_bundle_indices = lines_RASMM_2_VOX_indices(cur_bundle, cur_mask_nii.affine)
        #
        #     cur_end_points_indices = lines_RASMM_2_VOX_indices(cur_end_points, aparc_nii.affine)
        #
        #     no_class_count = 0
        #     wrong_class_total_count = 0
        #     wrong_class = dict()
        #
        #     no_class_tck = []
        #     wrong_class_tck = dict()
        #
        #     for index, line_indices, end_points in zip(range(len(cur_bundle)), cur_bundle_indices, cur_end_points_indices):
        #         cur_class = get_single_fiber_class(line_indices, end_points, cur_mask, cur_end_points_mask, aparc_atlas, bundle_names, combos)
        #         if cur_class == -1 or cur_class == -2:
        #             no_class_count += 1
        #             no_class_tck.append(cur_bundle[index])
        #         elif cur_class != i:
        #             wrong_class_total_count += 1
        #             if bundle_names[cur_class] not in wrong_class:
        #                 wrong_class[bundle_names[cur_class]] = 1
        #                 wrong_class_tck[bundle_names[cur_class]] = []
        #             else:
        #                 wrong_class[bundle_names[cur_class]] += 1
        #             wrong_class_tck[bundle_names[cur_class]].append(cur_bundle[index])
        #
        #     if len(no_class_tck) > 0:
        #         no_class_sft = StatefulTractogram(no_class_tck, cur_mask_path, cur_sft.space)
        #         save_tractogram(no_class_sft, os.path.join(cur_out_base_path, "no_class.tck"), bbox_valid_check=False)
        #
        #     if len(wrong_class_tck.keys()) > 0:
        #         for item in wrong_class_tck.keys():
        #             item_sft = StatefulTractogram(wrong_class_tck[item], cur_mask_path, cur_sft.space)
        #             save_tractogram(item_sft, os.path.join(cur_out_base_path, f"{item}.tck"), bbox_valid_check=False)
        #
        #     print(bundle_name, f"total_count: {len(cur_bundle)}", f"no_class_count: {no_class_count}, wrong_class_count: {wrong_class_total_count}")
        #     print(wrong_class)

            # break
        # break



if __name__ == '__main__':
    main()
