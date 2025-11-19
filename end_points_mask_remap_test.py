"""
    coding: utf-8
    Project: Fiber_Query
    File: end_points_mask_remap_test.py
    Author: xieyu
    Date: 2025/8/12 15:08
    IDE: PyCharm
"""

from utils import end_points_mask_remap
import nibabel as nib
import numpy as np


def main():
    data_nii = nib.load("/media/UG3/xieyu/tractography_generate/HCP/HCP_end_points_multi_mask/599469.nii.gz")
    data = data_nii.get_fdata().astype(int)

    remap_results = end_points_mask_remap(data)

    result_nii = nib.Nifti1Image(remap_results, affine=data_nii.affine, header=data_nii.header)

    nib.save(result_nii, "/media/UG3/xieyu/tractography_generate/HCP/599469_end_points_remap2.nii.gz" )


    pass


if __name__ == '__main__':
    main()
