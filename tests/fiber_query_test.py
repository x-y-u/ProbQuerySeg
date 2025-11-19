"""
    coding: utf-8
    Project: Fiber_Query
    File: fiber_query_BTC.py
    Author: xieyu
    Date: 2025/9/24 10:33
    IDE: PyCharm
"""
import os

import nibabel as nib
import numpy as np
from dipy.io.stateful_tractogram import StatefulTractogram
from dipy.io.streamline import save_tractogram

from tqdm import tqdm

from utils import get_bundle_names, get_single_fiber_class, read_lines, get_end_points, \
    lines_RASMM_2_VOX_indices, read_combos_as_map, get_single_fiber_class_simple


def main():
    tck_base_path = "/media/UG3/xieyu/fiber_query/HCPA/tracking_results/"

    mask_base_path = "/media/UG3/xieyu/fiber_query/HCPA/population_multi_mask_in_person/"
    end_points_mask_base_path = "/media/UG3/xieyu/fiber_query/HCPA/population_end_points_multi_mask_in_person/"

    extended_aparc_base_path = "/media/UG3/xieyu/fiber_query/HCPA/extended_aparc/"

    # out_base_path = "/media/UG3/xieyu/tractography_generate/HCP/recognize_results/"

    out_base_path = "/media/UG3/xieyu/fiber_query/HCPA/fiber_recognize_results/"

    sample_names = os.listdir(tck_base_path)

    sample_names = ['8724991']

    bundle_names = get_bundle_names()

    combos = read_combos_as_map("/media/UG3/xieyu/fiber_query/HCP/HCP_max_probability_pair/", bundle_names)

    tracking_types = [
        # 'track_ifod2_rk4_wmgmi_1M_step_30',
        'track_ifod1_rk4_dynamic_1M',
        # 'track_ifod1_rk4_seed_1M',
        # 'track_ifod1_rk4_dynamic_1M_step_30',
        # 'track_ifod1_rk4_seed_1M_step_30',
        # 'track_ifod1_rk4_wmgmi_1M',
        # 'track_ifod1_rk4_wmgmi_1M_step_30',
        # 'track_ifod2_rk4_wmgmi_1M',
        # 'track'
    ]

    for sample_name in tqdm(sample_names):
        print(sample_name)

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

        for tracking_type in tracking_types:
            # if os.path.exists(os.path.join(out_base_path, sample_name, f"fiber_query_labels-{tracking_type}.npy")):
            #     continue
            cur_whole_brain_path = "/media/UG3/xieyu/fiber_query/HCPA/fiber_recognize_results/8724991/fss_10k_results-track_ifod1_rk4_dynamic_1M/ATR_left.tck"

            cur_whole_brain_sft = read_lines(cur_whole_brain_path, cur_mask_path)
            cur_whole_brain_tck = cur_whole_brain_sft.streamlines

            cur_end_points = get_end_points(cur_whole_brain_tck)

            cur_bundle_indices = lines_RASMM_2_VOX_indices(cur_whole_brain_tck, cur_mask_nii.affine)

            cur_end_points_indices = lines_RASMM_2_VOX_indices(cur_end_points, cur_end_points_mask_nii.affine)

            cur_combo_points_indices = lines_RASMM_2_VOX_indices(cur_end_points, aparc_nii.affine)
            # print(cur_combo_points_indices)

            results = np.zeros((len(cur_whole_brain_tck), cur_mask.shape[3]))

            for index, line_indices, end_points, cur_combo_points in tqdm(zip(range(len(cur_whole_brain_tck)), cur_bundle_indices,
                                                       cur_end_points_indices, cur_combo_points_indices)):
                cur_class = get_single_fiber_class_simple(line_indices, end_points, cur_combo_points, cur_mask, cur_end_points_mask, aparc_atlas,
                                                   bundle_names, combos, 2)
                print(cur_class)
                if cur_class == -1 or cur_class == -2:
                    pass
                else:
                    results[index, cur_class] = 1

            # if not os.path.exists(os.path.join(out_base_path, sample_name)):
            #     os.makedirs(os.path.join(out_base_path, sample_name))
            #
            # np.save(os.path.join(out_base_path, sample_name, f"fiber_query_labels-{tracking_type}.npy"), results)


if __name__ == '__main__':
    main()
