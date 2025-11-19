"""
    coding: utf-8
    Project: Fiber_Query
    File: mask_plus&filter&norm.py
    Author: xieyu
    Date: 2025/9/3 10:52
    IDE: PyCharm
"""
import os

import numpy as np
import nibabel as nib
from scipy.ndimage import uniform_filter
from tqdm import tqdm

from utils import get_bundle_names


def fill_zeros_with_local_mean(image):
    """
    输入：
        image: 4D numpy array (shape: X, Y, Z)，整数类型
    输出：
        filled_image: 4D numpy array，空洞已填补
    """
    filled_image = np.copy(image)

    # 创建 mask: 非零区域为1，零为0
    zero_mask = (image == 0)

    # 计算均值（非零区域被平均，零区域仍为0）
    local_mean = uniform_filter(image.astype(np.float32), size=3, mode='constant', cval=0)

    filled_image[zero_mask] = local_mean[zero_mask]

    return filled_image


def main():

    base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_end_points_mask_reg/"

    out_base_path = "/media/UG3/xieyu/tractography_generate/HCP/MNI_end_points_probability_mask/"

    sample_names = os.listdir(base_path)

    bundle_names = get_bundle_names()

    for bundle_name in tqdm(bundle_names):
        all_mask = None

        header = None
        affine = None

        for sample_name in tqdm(sample_names):
            if header == None:
                cur_nii = nib.load(os.path.join(base_path, sample_name, f"{bundle_name}.nii.gz"))
                header = cur_nii.header
                affine = cur_nii.affine
                all_mask = cur_nii.get_fdata()
            else:
                all_mask = all_mask + nib.load(os.path.join(base_path, sample_name, f"{bundle_name}.nii.gz")).get_fdata()

        # mask_plus = np.sum(all_mask, axis=0)

        all_mask_filtered = fill_zeros_with_local_mean(all_mask)

        all_mask_filtered = all_mask_filtered / 105

        all_mask_filtered_nii = nib.Nifti1Image(all_mask_filtered, affine=affine, header=header)
        nib.save(all_mask_filtered_nii, os.path.join(out_base_path, f"{bundle_name}.nii.gz"))

    pass


if __name__ == '__main__':
    main()
