"""
    coding: utf-8
    Project: Fiber_Query
    File: plus_mask_filter&norm.py
    Author: xieyu
    Date: 2025/8/26 16:37
    IDE: PyCharm
"""

import numpy as np
import nibabel as nib
from scipy.ndimage import uniform_filter


def fill_zeros_with_local_mean(image):
    """
    输入：
        image: 4D numpy array (shape: X, Y, Z, C)，整数类型
    输出：
        filled_image: 4D numpy array，空洞已填补
    """
    filled_image = np.copy(image)
    x, y, z, c = image.shape

    for ch in range(c):
        channel_data = image[..., ch]

        # 创建 mask: 非零区域为1，零为0
        zero_mask = (channel_data == 0)

        # 计算均值（非零区域被平均，零区域仍为0）
        local_mean = uniform_filter(channel_data.astype(np.float32), size=3, mode='constant', cval=0)

        filled_image[..., ch][zero_mask] = local_mean[zero_mask]

    return filled_image


def main():
    in_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_plus/multi_mask_plus.nii.gz"
    out_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_plus/multi_mask_plus_filtered_norm.nii.gz"

    mask_nii = nib.load(in_path)

    origin_mask = mask_nii.get_fdata()

    mask_filled = fill_zeros_with_local_mean(origin_mask)

    mask_norm = mask_filled / 105

    norm_nii = nib.Nifti1Image(mask_norm, affine=mask_nii.affine, header=mask_nii.header)

    nib.save(norm_nii, out_path)

    pass


if __name__ == '__main__':
    main()
