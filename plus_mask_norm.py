"""
    coding: utf-8
    Project: Fiber_Query
    File: plus_mask_norm.py
    Author: xieyu
    Date: 2025/8/26 15:42
    IDE: PyCharm
"""

import numpy as np
import nibabel as nib


def main():

    in_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_plus/multi_mask_plus.nii.gz"
    out_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_plus/multi_mask_plus_norm.nii.gz"

    mask_nii = nib.load(in_path)

    origin_mask = mask_nii.get_fdata()

    origin_mask /= 105

    norm_mask_nii = nib.Nifti1Image(origin_mask, affine=mask_nii.affine, header=mask_nii.header)

    nib.save(norm_mask_nii, out_path)


    pass


if __name__ == '__main__':
    main()
