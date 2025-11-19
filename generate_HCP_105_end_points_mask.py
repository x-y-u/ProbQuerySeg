"""
    coding: utf-8
    Project: Fiber_Query
    File: generate_HCP_105_mask.py
    Author: xieyu
    Date: 2025/8/6 11:26
    IDE: PyCharm
"""
import os

from tqdm import tqdm
from generate_mask import generate_endpoint_mask


def main():
    dwi_base_path = "/media/UG5/HCP/"

    tck_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_tracts_tck/"
    out_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_end_points_mask/"

    sample_names = os.listdir(tck_base_path)

    for sample_name in tqdm(sample_names):
        print(sample_name)

        org_file_path = os.path.join(dwi_base_path, sample_name, f"T1w/Diffusion/data.nii.gz")

        cur_tck_base_path = os.path.join(tck_base_path, sample_name, "tracts")

        cur_out_base_path = os.path.join(out_base_path, sample_name)
        if not os.path.exists(cur_out_base_path):
            os.makedirs(cur_out_base_path)

        bundle_names = os.listdir(cur_tck_base_path)
        for bundle_name in tqdm(bundle_names):
            cur_tck_path = os.path.join(cur_tck_base_path, bundle_name)
            cur_out_path = os.path.join(cur_out_base_path, bundle_name.replace('.tck', ".nii.gz"))
            generate_endpoint_mask(cur_tck_path, org_file_path, cur_out_path)


if __name__ == '__main__':
    main()
