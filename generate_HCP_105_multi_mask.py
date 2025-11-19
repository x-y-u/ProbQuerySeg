"""
    coding: utf-8
    Project: Fiber_Query
    File: generate_HCP_105_multi_mask.py
    Author: xieyu
    Date: 2025/8/7 10:50
    IDE: PyCharm
"""


import os

import nibabel as nib

import numpy as np
from tqdm import tqdm
from utils import get_bundle_names, merge_mask


# def merge_mask(base_path, out_path):
#     bundles = get_bundle_names()
#
#     ref_img = nib.load(os.path.join(base_path, f"{bundles[0]}.nii.gz"))
#     affine = ref_img.affine
#     header = ref_img.header.copy()
#
#     results = []
#
#     for bundle in bundles:
#         results.append(nib.load(os.path.join(base_path, f"{bundle}.nii.gz")).get_fdata())
#
#     results = np.stack(results, axis=-1)
#
#     out_nii = nib.Nifti1Image(results, affine=affine, header=header)
#
#     nib.save(out_nii, out_path)


def main():

    base_path = "/media/UG3/xieyu/fiber_query/HCPA/population_mask_in_person/"

    sample_names = os.listdir(base_path)

    out_base_path = "/media/UG3/xieyu/fiber_query/HCPA/population_multi_mask_in_person/"
    if not os.path.exists(out_base_path):
        os.makedirs(out_base_path)

    for sample_name in tqdm(sample_names):
        merge_mask(os.path.join(base_path, sample_name), os.path.join(out_base_path, f"{sample_name}.nii.gz"))

    base_path = "/media/UG3/xieyu/fiber_query/HCPA/population_end_points_mask_in_person/"

    sample_names = os.listdir(base_path)

    out_base_path = "/media/UG3/xieyu/fiber_query/HCPA/population_end_points_multi_mask_in_person/"
    if not os.path.exists(out_base_path):
        os.makedirs(out_base_path)

    for sample_name in tqdm(sample_names):
        merge_mask(os.path.join(base_path, sample_name), os.path.join(out_base_path, f"{sample_name}.nii.gz"))

    base_path = "/media/UG3/xieyu/fiber_query/HCPD/population_mask_in_person/"

    sample_names = os.listdir(base_path)

    out_base_path = "/media/UG3/xieyu/fiber_query/HCPD/population_multi_mask_in_person/"
    if not os.path.exists(out_base_path):
        os.makedirs(out_base_path)

    for sample_name in tqdm(sample_names):
        merge_mask(os.path.join(base_path, sample_name), os.path.join(out_base_path, f"{sample_name}.nii.gz"))

    base_path = "/media/UG3/xieyu/fiber_query/HCPD/population_end_points_mask_in_person/"

    sample_names = os.listdir(base_path)

    out_base_path = "/media/UG3/xieyu/fiber_query/HCPD/population_end_points_multi_mask_in_person/"
    if not os.path.exists(out_base_path):
        os.makedirs(out_base_path)

    for sample_name in tqdm(sample_names):
        merge_mask(os.path.join(base_path, sample_name), os.path.join(out_base_path, f"{sample_name}.nii.gz"))


if __name__ == '__main__':
    main()
