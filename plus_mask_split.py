"""
    coding: utf-8
    Project: Fiber_Query
    File: plus_mask_split.py
    Author: xieyu
    Date: 2025/8/31 17:27
    IDE: PyCharm
"""

import nibabel as nib
import os
from utils import get_bundle_names

def split_nii_channels(input_path, output_dir, bundle_names):
    # 读取 NIfTI 文件
    img = nib.load(input_path)
    data = img.get_fdata()
    affine = img.affine
    header = img.header

    # 检查是否为 4D (X,Y,Z,C)
    if data.ndim != 4:
        raise ValueError(f"输入数据 shape={data.shape}，不是 (X,Y,Z,C) 格式")

    n_channels = data.shape[3]
    assert n_channels == len(bundle_names), "n_channels={} != len(bundle_names)".format(n_channels)
    print(f"图像 shape={data.shape}，共有 {n_channels} 个通道")

    os.makedirs(output_dir, exist_ok=True)

    for c in range(n_channels):
        channel_data = data[..., c]  # 取第 c 个通道
        channel_img = nib.Nifti1Image(channel_data, affine, header)
        out_path = os.path.join(output_dir, f"{bundle_names[c]}.nii.gz")
        nib.save(channel_img, out_path)
        print(f"已保存: {out_path}")


def main():

    bundle_names = get_bundle_names()

    # 示例调用
    split_nii_channels("/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_reg_plus/multi_mask_plus_filtered_norm.nii.gz", "/media/UG3/xieyu/tractography_generate/HCP/MNI_bundle_probability_mask/", bundle_names)

    pass


if __name__ == '__main__':
    main()
