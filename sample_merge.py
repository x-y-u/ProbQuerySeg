"""
    coding: utf-8
    Project: Fiber_Query
    File: sample_merge.py
    Author: xieyu
    Date: 2025/9/15 10:20
    IDE: PyCharm
"""


import os
import glob
import random
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.io.stateful_tractogram import StatefulTractogram, Space
import nibabel as nib

def sample_streamlines(tck_file, reference, max_num=5000):
    """从一个tck文件里读取纤维，如果数量大于max_num则采样"""
    tractogram = load_tractogram(tck_file, reference=reference, bbox_valid_check=False)
    streamlines = list(tractogram.streamlines)
    if len(streamlines) > max_num:
        streamlines = random.sample(streamlines, max_num)
    return streamlines


def merge_across_subjects(root_dir, output_dir, ref_nifti, max_num=5000):
    os.makedirs(output_dir, exist_ok=True)

    # 找到所有样本目录
    subjects = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    if not subjects:
        print("❌ 没有发现样本目录")
        return

    # 用第一个样本目录里的tck名字作为标准
    example_dir = os.path.join(root_dir, subjects[0])
    fiber_files = sorted(glob.glob(os.path.join(example_dir, "*.tck")))
    fiber_names = [os.path.basename(f) for f in fiber_files]

    print(f"发现纤维束: {fiber_names}")

    ref_img = nib.load(ref_nifti)

    # 对每个纤维束分别处理
    for fname in fiber_names:
        all_streamlines = []

        for sub in subjects:
            fpath = os.path.join(root_dir, sub, fname)
            if os.path.exists(fpath):
                try:
                    streamlines = sample_streamlines(fpath, ref_img, max_num=max_num)
                    all_streamlines.extend(streamlines)
                except Exception as e:
                    print(f"读取 {fpath} 失败: {e}")

        if not all_streamlines:
            print(f"⚠️ 没有找到 {fname}")
            continue

        print(f"{fname}: 合并后 {len(all_streamlines)} 条纤维")

        # 保存合并结果
        sft = StatefulTractogram(all_streamlines, ref_img, Space.RASMM)
        save_tractogram(sft, os.path.join(output_dir, fname), bbox_valid_check=False)


def main():
    # ================= 使用示例 =================
    root_dir = "/media/UG3/xieyu/fiber_query/HCP/MNI_tck"  # 每个子目录是一个样本
    output_dir = "/media/UG3/xieyu/fiber_query/HCP/merged_MNI_tck"
    ref_nifti = "/media/UG3/xieyu/fiber_query/HCP/T1_un_reg/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii"

    merge_across_subjects(root_dir, output_dir, ref_nifti, max_num=3000)
    pass


if __name__ == '__main__':
    main()
