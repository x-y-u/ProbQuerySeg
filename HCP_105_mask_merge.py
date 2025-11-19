"""
    coding: utf-8
    Project: Fiber_Query
    File: HCP_105_mask_merge.py
    Author: xieyu
    Date: 2025/8/7 10:37
    IDE: PyCharm
"""
import os

import nibabel as nib

import numpy as np
from tqdm import tqdm


def merge_mask(base_path, out_path):
    bundles = os.listdir(base_path)

    base_nii = nib.load(os.path.join(base_path, bundles[0]))
    base_img = base_nii.get_fdata()

    base_affine = base_nii.affine

    for bundle in bundles[1:]:
        base_img += nib.load(os.path.join(base_path, bundle)).get_fdata()

    out_nii = nib.Nifti1Image(base_img, base_affine)
    nib.save(out_nii, out_path)


def main():

    base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_mask/"

    sample_names = os.listdir(base_path)

    out_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_merged_mask/"
    if not os.path.exists(out_base_path):
        os.makedirs(out_base_path)

    for sample_name in tqdm(sample_names):
        merge_mask(os.path.join(base_path, sample_name), os.path.join(out_base_path, f"{sample_name}.nii.gz"))


if __name__ == '__main__':
    main()
