"""
    coding: utf-8
    Project: Fiber_Query
    File: probability_mask_to_label.py
    Author: xieyu
    Date: 2025/9/4 15:48
    IDE: PyCharm
"""
import numpy as np
import nibabel as nib
from tqdm import tqdm

from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import hamming


def merge_small_segments(unique_combos, order, inverse_idx, min_voxels):
    """
    将聚类叶子按顺序划分成多个子序列，每个子序列的体素数 >= min_voxels。
    如果小于，就与左右最近的子序列合并（按汉明距离最近）。

    Parameters
    ----------
    unique_combos : np.ndarray, shape=(n_unique, C)
        唯一组合（0/1数组）。
    order : np.ndarray, shape=(n_unique,)
        聚类叶子顺序（leaves_list(Z) 得到的索引）。
    inverse_idx : np.ndarray, shape=(N_voxels,)
        每个体素对应的唯一组合索引。
    min_voxels : int
        每个子序列的最小体素数量。

    Returns
    -------
    segments : list of dict
        每个子序列的信息，包含：
        {
          "indices": [叶子索引们],
          "count": 总体素数
        }
    """
    # 每个唯一组合的体素数
    counts = np.bincount(inverse_idx, minlength=len(unique_combos))

    print("counts:", counts)


    # 初始化子序列（每个叶子一个 segment）
    segments = [{"indices": [i], "count": counts[i]} for i in order]

    # print(len(segments))

    changed = True
    while changed:
        changed = False
        i = 0
        # print("change", 1)
        while i < len(segments):
            seg = segments[i]
            # print(seg['indices'])
            # print(seg['count'])
            if seg["count"] >= min_voxels:
                i += 1
                continue

            # seg 太小，需要合并
            left_dist = right_dist = np.inf
            left_idx = right_idx = None

            # 和左边的最后一个比较
            if i > 0:
                left_leaf = segments[i - 1]["indices"][-1]
                cur_leaf = seg["indices"][0]
                left_dist = hamming(unique_combos[left_leaf], unique_combos[cur_leaf])
                left_idx = i - 1

            # 和右边的第一个比较
            if i < len(segments) - 1:
                right_leaf = segments[i + 1]["indices"][0]
                cur_leaf = seg["indices"][-1]
                right_dist = hamming(unique_combos[right_leaf], unique_combos[cur_leaf])
                right_idx = i + 1

            # 选择更近的方向合并
            if left_dist < right_dist and left_idx is not None:
                segments[left_idx]["indices"].extend(seg["indices"])
                segments[left_idx]["count"] += seg["count"]
                changed = True
                segments[i]['count'] = 0
                # print(i, "left")
                break
            elif right_idx is not None:
                segments[right_idx]["indices"] = seg["indices"] + segments[right_idx]["indices"]
                # print(segments[right_idx]["count"])
                segments[right_idx]["count"] += seg["count"]
                # print(segments[right_idx]["count"])
                changed = True
                segments[i]['count'] = 0
                i += 1  # 跳过右边的，因为已合并
                # print(i, "right")
                break
            else:
                pass

            i += 1

        # 把未合并的保留下来
        # 注意：合并逻辑里有修改，new_segments 只保留没动过的
        # 所以最终结果要从 segments 更新
        segments = [s for s in segments if s["count"] > 0]

    return segments


def multi_channel_to_label_cluster(arr, threshold=0.6, min_voxels=500):
    """
    arr: (D,H,W,C)，值 ∈ [0,1]
    返回: (D,H,W) 标签数组 + 组合映射
    """
    # Step 1: 二值化
    bin_arr = (arr > threshold).astype(np.int8)
    D, H, W, C = bin_arr.shape
    origin_flat = bin_arr.reshape(-1, C)

    nonzero_mask = origin_flat.any(axis=1)
    flat = origin_flat[nonzero_mask]

    # Step 2: 找到所有唯一组合
    unique_combos, inverse_idx = np.unique(flat, axis=0, return_inverse=True)

    print(len(unique_combos))

    # Step 3: 对唯一组合做层次聚类（汉明距离）
    Z = linkage(unique_combos, method="average", metric="hamming")
    order = leaves_list(Z)  # 聚类叶子顺序

    # Step 4: 生成组合 → 标签映射
    # combo_to_label = {tuple(unique_combos[i]): idx + 1000 for idx, i in enumerate(order)}

    segments = merge_small_segments(unique_combos, order, inverse_idx, min_voxels)

    print(len(segments))

    combo_to_label = {}

    cur_label = 1000

    for seg in segments:
        for index in seg["indices"]:
            combo_to_label[tuple(unique_combos[index])] = cur_label
        cur_label += len(seg["indices"])

    print(cur_label)

    combo_to_label[tuple(np.zeros(C, dtype=np.int32))] = 0

    labels = np.zeros(origin_flat.shape[0], dtype=np.int32)

    for i, row in tqdm(enumerate(origin_flat)):
        labels[i] += combo_to_label[tuple(row)]

    # # Step 5: 根据映射生成标签数组
    # labels = np.array([combo_to_label[tuple(row)] for row in flat], dtype=np.int32)
    # labels = labels.reshape(D, H, W)

    return labels.reshape(D, H, W), combo_to_label


def main():

    in_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/multi_mask_plus_filtered_norm.nii.gz"
    out_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/multi_mask_label2.nii.gz"

    origin_image_nii = nib.load(in_path)

    origin_image = origin_image_nii.get_fdata()

    new_image, unique_combos = multi_channel_to_label_cluster(origin_image, threshold=0.15, min_voxels=300)

    print(len(unique_combos))

    new_image_nii = nib.Nifti1Image(new_image, affine=origin_image_nii.affine)
    nib.save(new_image_nii, out_path)


if __name__ == '__main__':
    main()
