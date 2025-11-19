"""
    coding: utf-8
    Project: Fiber_Query
    File: get_bundle_connection_combo.py
    Author: xieyu
    Date: 2025/8/12 11:32
    IDE: PyCharm
"""

import os

import nibabel as nib

from tqdm import tqdm

from utils import get_bundle_names, read_lines_as_vox_indices, get_bundle_connection, get_bundle_combo, read_lines, \
    get_end_points, lines_RASMM_2_VOX_indices, write_connection_dicts


def main():

    dwi_base_path = "/media/UG5/HCP/"

    tck_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_tracts_tck/"

    out_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_connection_pair/"

    extended_aparc_base_path = "/media/UG3/xieyu/tractography_generate/HCP/extended_aparc/"

    sample_names = os.listdir(tck_base_path)

    # sample_names = ["599469"]

    bundle_names = get_bundle_names()

    for sample_name in tqdm(sample_names):
        # aparc_file_path = os.path.join(dwi_base_path, sample_name, f"T1w/aparc.a2009s+aseg.nii.gz")

        aparc_file_path = os.path.join(extended_aparc_base_path, f"{sample_name}.nii.gz")

        cur_aparc_nii = nib.load(aparc_file_path)

        cur_tck_base_path = os.path.join(tck_base_path, sample_name, "tracts")

        cur_out_base_path = os.path.join(out_base_path, sample_name)
        if not os.path.exists(cur_out_base_path):
            os.makedirs(cur_out_base_path)

        for i, bundle_name in tqdm(enumerate(bundle_names)):
            cur_bundle_path = os.path.join(cur_tck_base_path, f"{bundle_name}.tck")

            cur_bundle = read_lines(cur_bundle_path, aparc_file_path).streamlines

            cur_bundle_end_points = get_end_points(cur_bundle)

            cur_bundle_end_points_indices = lines_RASMM_2_VOX_indices(cur_bundle_end_points, cur_aparc_nii.affine)

            cur_connection = get_bundle_connection(cur_bundle_end_points_indices, cur_aparc_nii.get_fdata().astype(int))

            write_connection_dicts(cur_connection, os.path.join(cur_out_base_path, f"{bundle_name}.txt"))


if __name__ == '__main__':
    main()
