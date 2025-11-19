"""
    coding: utf-8
    Project: Fiber_Query
    File: cluster_smooth.py
    Author: xieyu
    Date: 2025/10/15 16:30
    IDE: PyCharm
"""

import numpy as np
import nibabel as nib

from scipy.ndimage import label
from tqdm import tqdm
from scipy.ndimage import generic_filter


def remove_small_clusters(labels_3d, min_size=20):
    """
    移除每个类别中小于 min_size 的连通块，并记录被清除的体素。
    返回：
      cleaned: 清除后的标签体积
      removed_mask: 被清除体素的布尔掩膜（True 表示被清除）
    """
    cleaned = np.zeros_like(labels_3d)
    removed_mask = np.zeros_like(labels_3d, dtype=bool)

    for k in tqdm(np.unique(labels_3d)):
        if k == 0:
            continue
        binary = (labels_3d == k)
        labeled, num = label(binary)
        for i in range(1, num + 1):
            region_mask = (labeled == i)
            region_size = np.sum(region_mask)
            if region_size >= min_size:
                cleaned[region_mask] = k
            else:
                removed_mask[region_mask] = True  # 标记被清除的部分

    return cleaned, removed_mask


def hole_fill_filter(volume, removed_mask, size=3, neighbor_thresh=5):
    """
    仅对 removed_mask 中的体素进行条件多数投票填补：
    - 只填补被清除的空洞；
    - 对非 removed_mask 区域不做处理。
    """
    def conditional_vote(values):
        center = values[len(values) // 2]
        vals, counts = np.unique(values, return_counts=True)

        # 去掉 0（无标签）的计数
        nonzero_mask = vals != 0
        nonzero_counts = counts[nonzero_mask]
        nonzero_vals = vals[nonzero_mask]

        if len(nonzero_vals) == 0:
            return center  # 邻域全是 0，不处理

        # 如果周围有足够数量的有标签体素
        if np.sum(nonzero_counts) >= neighbor_thresh:
            return nonzero_vals[np.argmax(nonzero_counts)]
        else:
            return center

    # 只对 removed_mask 区域应用滤波
    filled = volume.copy()
    # sub_volume = volume.copy()
    # sub_volume[~removed_mask] = 0  # 避免非目标区域参与滤波

    filtered = generic_filter(
        volume,
        conditional_vote,
        size=size,
        mode='nearest'
    )

    # 只在 removed_mask 区域更新结果
    filled[removed_mask] = filtered[removed_mask]
    return filled


def label_smooth(volume, size=3, neighbor_thresh=5):
    def conditional_vote(values):
        center = values[len(values) // 2]
        vals, counts = np.unique(values, return_counts=True)

        # 去掉 0（无标签）的计数
        nonzero_mask = vals != 0
        nonzero_counts = counts[nonzero_mask]
        nonzero_vals = vals[nonzero_mask]

        if len(nonzero_vals) == 0:
            return center  # 邻域全是 0，不处理

        # 如果周围有足够数量的有标签体素
        if np.sum(nonzero_counts) >= neighbor_thresh:
            return nonzero_vals[np.argmax(nonzero_counts)]
        else:
            return center

    filtered = generic_filter(
        volume,
        conditional_vote,
        size=size,
        mode='nearest'
    )

    return filtered


def main():

    # cluster_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/end_points_multi_mask_cluster_100.nii.gz"
    # out_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/end_points_multi_mask_cluster_100_smoothed.nii.gz"
    #
    # cluster_nii = nib.load(cluster_path)
    # cluster_img = cluster_nii.get_fdata()
    #
    # labels_cleaned, removed_mask = remove_small_clusters(cluster_img, min_size=30)
    #
    # labels_cleaned_filled = hole_fill_filter(labels_cleaned, removed_mask, size=3, neighbor_thresh=5)
    #
    # new_image_nii = nib.Nifti1Image(labels_cleaned_filled, affine=cluster_nii.affine)
    # nib.save(new_image_nii, out_path)

    cluster_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/multi_mask_label_smoothed.nii.gz"
    out_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/multi_mask_label_smoothed_filtered.nii.gz"

    cluster_nii = nib.load(cluster_path)
    cluster_img = cluster_nii.get_fdata()

    labels_cleaned_filled = label_smooth(cluster_img, size=3, neighbor_thresh=5)

    new_image_nii = nib.Nifti1Image(labels_cleaned_filled, affine=cluster_nii.affine)
    nib.save(new_image_nii, out_path)


if __name__ == '__main__':
    main()
