"""
    coding: utf-8
    Project: Fiber_Query
    File: count_combo.py
    Author: xieyu
    Date: 2025/8/7 10:58
    IDE: PyCharm
"""
import numpy as np
from collections import Counter
import nibabel as nib

def main():

    # 假设你的四维数组如下（元素值为0或1）
    # shape = (X, Y, Z, C)
    data = nib.load("/media/UG3/xieyu/tractography_generate/HCP/HCP_end_points_multi_mask/599469.nii.gz").get_fdata()

    # 获取最后一维通道的 axis
    C = data.shape[-1]


    # 将所有通道组合为元组形式，方便统计
    # Step 1: reshape 为 (-1, C)，即每个体素一行
    reshaped = data.reshape(-1, C)

    # Step 2: 找出为1的通道组合
    # 每一行 → 找出为1的索引 → 转成tuple（方便hash）
    combinations = [tuple(np.flatnonzero(row)) for row in reshaped if np.any(row)]

    # Step 3: 统计所有组合
    combo_counter = Counter(combinations)
    print(len(combo_counter.items()))

    top_1000 = combo_counter.most_common(1000)

    print(top_1000[999])

    # 打印结果
    # for combo, count in combo_counter.items():
    #     print(f"通道组合 {combo} 出现次数：{count}")

    pass


if __name__ == '__main__':
    main()
