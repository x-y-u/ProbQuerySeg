"""
    coding: utf-8
    Project: Fiber_Query
    File: reg_result_plus.py
    Author: xieyu
    Date: 2025/8/25 18:07
    IDE: PyCharm
"""
import os

import nibabel as nib
import numpy as np
from tqdm import tqdm


def main():

    base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_end_points_multi_mask_reg/"
    out_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_end_points_multi_mask_reg_plus/multi_mask_plus.nii.gz"

    all_mask = None

    header = None
    affine = None

    for subject in tqdm(os.listdir(base_path)):
        if header == None:
            cur_nii = nib.load(os.path.join(base_path, subject))
            header = cur_nii.header
            affine = cur_nii.affine
            all_mask = cur_nii.get_fdata()
        else:
            all_mask = all_mask + nib.load(os.path.join(base_path, subject)).get_fdata()

    # mask_plus = np.sum(all_mask, axis=0)

    mask_plus_nii = nib.Nifti1Image(all_mask, affine=affine, header=header)
    nib.save(mask_plus_nii, out_path)

    pass


if __name__ == '__main__':
    main()
