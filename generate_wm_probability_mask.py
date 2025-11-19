"""
    coding: utf-8
    Project: Fiber_Query
    File: generate_wm_probability_mask.py
    Author: xieyu
    Date: 2025/10/19 17:57
    IDE: PyCharm
"""
import numpy as np

import nibabel as nib


def main():

    probability_mask_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/multi_mask_plus_filtered_norm.nii.gz"

    out_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/wm_multi_mask_plus_filtered_norm.nii.gz"

    aparc_path = "/media/UG5/Atlas/MNI/freesurfer/mri/aparc.a2009s+aseg.nii.gz"

    aparc_nii = nib.load(aparc_path)

    aparc_img = aparc_nii.get_fdata().astype(int)

    probability_mask_nii = nib.load(probability_mask_path)

    probability_mask = probability_mask_nii.get_fdata()

    new_mask = probability_mask * (((aparc_img == 41) + (aparc_img == 2))[..., np.newaxis])

    new_mask_nii = nib.Nifti1Image(new_mask, affine=aparc_nii.affine, header=aparc_nii.header)

    nib.save(new_mask_nii, out_path)


if __name__ == '__main__':
    main()
