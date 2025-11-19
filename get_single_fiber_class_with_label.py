"""
    coding: utf-8
    Project: Fiber_Query
    File: get_single_fiber_class_with_label.py
    Author: xieyu
    Date: 2025/9/8 11:14
    IDE: PyCharm
"""


import os

import nibabel as nib
from dipy.io.stateful_tractogram import StatefulTractogram
from dipy.io.streamline import save_tractogram

from tqdm import tqdm

from utils import get_bundle_names, get_single_fiber_class_with_label, read_lines_as_vox_indices, read_lines, get_end_points, \
    lines_RASMM_2_VOX_indices, read_combos_as_map, read_json


def main():

    tck_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_tracts_tck/"

    label_base_path = "/media/UG3/xieyu/tractography_generate/HCP/multi_mask_label_in_person/"
    end_points_label_base_path = "/media/UG3/xieyu/tractography_generate/HCP/end_points_multi_mask_label_in_person/"

    label_transform_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_reg_plus/multi_mask_label_transform.json"
    end_points_label_transform_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_reg_plus/end_points_multi_mask_label_transform.json"

    label_transform = read_json(label_transform_path)
    end_points_label_transform = read_json(end_points_label_transform_path)

    label_transform['0'] = [0] * 72
    end_points_label_transform['0'] = [0] * 72

    extended_aparc_base_path = "/media/UG3/xieyu/tractography_generate/HCP/extended_aparc/"

    out_base_path = "/media/UG3/xieyu/tractography_generate/HCP/recognize_results_with_label/"

    sample_names = os.listdir(tck_base_path)

    sample_names = ['896879']

    bundle_names = get_bundle_names()

    combos = read_combos_as_map("/media/UG3/xieyu/tractography_generate/HCP/HCP_max_probability_pair/", bundle_names)

    for sample_name in tqdm(sample_names):
        print(sample_name)

        cur_tck_base_path = os.path.join(tck_base_path, sample_name, "tracts")

        cur_label_path = os.path.join(label_base_path, f"{sample_name}.nii.gz")
        cur_label_nii = nib.load(cur_label_path)
        cur_label = cur_label_nii.get_fdata().astype(int)

        cur_end_points_label_path = os.path.join(end_points_label_base_path, f"{sample_name}.nii.gz")
        cur_end_points_label_nii = nib.load(cur_end_points_label_path)
        cur_end_points_label = cur_end_points_label_nii.get_fdata().astype(int)

        # aparc_file_path = os.path.join(dwi_base_path, sample_name, f"T1w/aparc.a2009s+aseg.nii.gz")
        aparc_file_path = os.path.join(extended_aparc_base_path, f"{sample_name}.nii.gz")
        aparc_nii = nib.load(aparc_file_path)
        aparc_atlas = aparc_nii.get_fdata().astype(int)

        for i, bundle_name in tqdm(enumerate(bundle_names)):

            cur_out_base_path = os.path.join(out_base_path, sample_name, bundle_name)
            if not os.path.exists(cur_out_base_path):
                os.makedirs(cur_out_base_path)

            cur_bundle_path = os.path.join(cur_tck_base_path, f"{bundle_name}.tck")

            cur_sft = read_lines(cur_bundle_path, cur_label_path)
            cur_bundle = cur_sft.streamlines

            cur_end_points = get_end_points(cur_bundle)

            cur_bundle_indices = lines_RASMM_2_VOX_indices(cur_bundle, cur_label_nii.affine)

            cur_end_points_indices = lines_RASMM_2_VOX_indices(cur_end_points, aparc_nii.affine)

            no_class_count = 0
            wrong_class_total_count = 0
            wrong_class = dict()

            no_class_tck = []
            wrong_class_tck = dict()

            for index, line_indices, end_points in zip(range(len(cur_bundle)), cur_bundle_indices, cur_end_points_indices):
                cur_class = get_single_fiber_class_with_label(line_indices, end_points, cur_label, cur_end_points_label,
                                                              label_transform, end_points_label_transform, aparc_atlas, bundle_names, combos, i)
                if cur_class == -1 or cur_class == -2:
                    no_class_count += 1
                    no_class_tck.append(cur_bundle[index])
                elif cur_class != i:
                    wrong_class_total_count += 1
                    if bundle_names[cur_class] not in wrong_class:
                        wrong_class[bundle_names[cur_class]] = 1
                        wrong_class_tck[bundle_names[cur_class]] = []
                    else:
                        wrong_class[bundle_names[cur_class]] += 1
                    wrong_class_tck[bundle_names[cur_class]].append(cur_bundle[index])

            if len(no_class_tck) > 0:
                no_class_sft = StatefulTractogram(no_class_tck, cur_label_path, cur_sft.space)
                save_tractogram(no_class_sft, os.path.join(cur_out_base_path, "no_class.tck"), bbox_valid_check=False)

            if len(wrong_class_tck.keys()) > 0:
                for item in wrong_class_tck.keys():
                    item_sft = StatefulTractogram(wrong_class_tck[item], cur_label_path, cur_sft.space)
                    save_tractogram(item_sft, os.path.join(cur_out_base_path, f"{item}.tck"), bbox_valid_check=False)

            print(bundle_name, f"total_count: {len(cur_bundle)}", f"no_class_count: {no_class_count}, wrong_class_count: {wrong_class_total_count}")
            print(wrong_class)

            # break
        break



if __name__ == '__main__':
    main()
