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
#     results = []
#
#     for bundle in bundles:
#         results.append(nib.load(os.path.join(base_path, f"{bundle}.nii.gz")).get_fdata())
#
#     results = np.stack(results, axis=-1)
#
#     out_nii = nib.Nifti1Image(results, np.eye(4))
#     nib.save(out_nii, out_path)


def main():

    base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_end_points_mask_reg/"

    sample_names = os.listdir(base_path)

    out_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_end_points_multi_mask_reg/"
    if not os.path.exists(out_base_path):
        os.makedirs(out_base_path)

    for sample_name in tqdm(sample_names):
        merge_mask(os.path.join(base_path, sample_name), os.path.join(out_base_path, f"{sample_name}.nii.gz"))


if __name__ == '__main__':
    main()
