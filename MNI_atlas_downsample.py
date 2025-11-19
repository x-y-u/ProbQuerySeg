"""
    coding: utf-8
    Project: Fiber_Query
    File: MNI_atlas_downsample.py
    Author: xieyu
    Date: 2025/9/15 11:02
    IDE: PyCharm
"""


import os
import glob
import random
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.io.stateful_tractogram import StatefulTractogram, Space
import nibabel as nib


def downsample_streamlines(streamlines, target_num):
    """对流线随机降采样"""
    if len(streamlines) > target_num:
        return random.sample(streamlines, target_num)
    else:
        return streamlines  # 不够 target_num 就全部保留


def downsample_merged_tcks(input_dir, output_dir, ref_nifti, sizes=(30000, 10000)):
    os.makedirs(output_dir, exist_ok=True)

    # 找到合并结果目录下所有 tck 文件
    tck_files = sorted(glob.glob(os.path.join(input_dir, "*.tck")))
    if not tck_files:
        print("❌ 没有找到合并结果 tck 文件")
        return

    ref_img = nib.load(ref_nifti)

    for fpath in tck_files:
        fname = os.path.basename(fpath)
        print(f"\n处理 {fname} ...")

        tractogram = load_tractogram(fpath, reference=ref_img, bbox_valid_check=False)
        streamlines = list(tractogram.streamlines)
        n_streams = len(streamlines)
        print(f"原始纤维数量: {n_streams}")

        for size in sizes:
            sampled = downsample_streamlines(streamlines, size)
            out_path = os.path.join(output_dir, f"{fname.replace('.tck', f'_{size//1000}k.tck')}")
            sft = StatefulTractogram(sampled, ref_img, Space.RASMM)
            save_tractogram(sft, out_path, bbox_valid_check=False)
            print(f"保存 {out_path}, 数量 {len(sampled)}")


def main():
    # ========== 使用示例 ==========
    input_dir = "/media/UG3/xieyu/fiber_query/HCP/merged_MNI_tck"  # 已合并结果
    output_dir = "/media/UG3/xieyu/fiber_query/HCP/merged_MNI_tck_downsampled"
    ref_nifti = "/media/UG3/xieyu/fiber_query/HCP/T1_un_reg/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii"

    downsample_merged_tcks(input_dir, output_dir, ref_nifti, sizes=(30000, 20000, 10000))
    pass


if __name__ == '__main__':
    main()
