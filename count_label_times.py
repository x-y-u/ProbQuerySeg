"""
    coding: utf-8
    Project: Fiber_Query
    File: count_label_times.py
    Author: xieyu
    Date: 2025/9/4 17:57
    IDE: PyCharm
"""

import numpy as np
import nibabel as nib


def bucket_label_counts(label_arr, bin_size=50):
    """
    label_arr: 单通道标签数组
    bin_size: 桶的大小，例如 100

    返回: dict {区间: 种类数量}
    """
    labels, counts = np.unique(label_arr, return_counts=True)

    print(len(labels))

    # 每个 label 按出现次数划分到桶
    bins = counts // bin_size  # e.g. 0→[0,100), 1→[100,200) ...

    result = {}
    for b in np.unique(bins):
        # 当前桶的范围
        start = b * bin_size
        end = start + bin_size
        key = f"[{start}, {end})"
        result[key] = np.sum(bins == b)

    return result


def main():

    data_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_reg_plus/end_points_multi_mask_label.nii.gz"

    data = nib.load(data_path).get_fdata().astype(int)

    count_results = bucket_label_counts(data)

    for k, v in count_results.items():
        print(f"{k}: {v}")

    pass


if __name__ == '__main__':
    main()
