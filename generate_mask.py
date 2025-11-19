"""
    coding: utf-8
    Project: Fiber_Query
    File: generate_mask.py
    Author: xieyu
    Date: 2025/8/6 11:12
    IDE: PyCharm
"""

import os
import subprocess


def generate_mask(tck_path, ref_img_path, output_mask_path):
    """
    用 MRtrix3 将 .tck 文件和参考图像生成掩膜图像（mask）

    参数:
        tck_path (str): 输入的 .tck 文件路径
        ref_img_path (str): 输入的参考图像 .nii 或 .nii.gz
        output_mask_path (str): 输出掩膜图像的路径（.nii.gz）
    """
    # 临时 density map 路径
    tmp_density_path = output_mask_path.replace('.nii.gz', '_tmp_density.nii.gz')

    # Step 1: 生成 density map
    cmd1 = [
        'tckmap',
        tck_path,
        '-template', ref_img_path,
        tmp_density_path
    ]

    # Step 2: 使用 mrthreshold 生成二值 mask
    cmd2 = [
        'mrthreshold',
        tmp_density_path,
        '-abs', '0.1',
        output_mask_path,
        '-force'
    ]

    # 执行命令
    try:
        subprocess.run(cmd1, check=True)
        subprocess.run(cmd2, check=True)
    finally:
        # 删除临时文件
        if os.path.exists(tmp_density_path):
            os.remove(tmp_density_path)


def generate_endpoint_mask(tck_path, ref_img_path, output_mask_path):
    """
    用 MRtrix3 将 .tck 文件的终点（endpoints）映射为 mask 图像

    参数:
        tck_path (str): 输入的 .tck 文件路径
        ref_img_path (str): 参考图像路径（.nii 或 .nii.gz）
        output_mask_path (str): 输出的 endpoint mask 路径（.nii.gz）
    """
    # 临时 endpoint density map 路径
    tmp_endpoint_path = output_mask_path.replace('.nii.gz', '_tmp_endpoint.nii.gz')

    # Step 1: 使用 tckmap 生成终点密度图（每条纤维的起点和终点位置）
    cmd1 = [
        'tckmap',
        '-ends_only',
        tck_path,
        '-template', ref_img_path,
        tmp_endpoint_path
    ]

    # Step 2: 转为二值 mask，只要有终点落在体素上就记为 1
    cmd2 = [
        'mrthreshold',
        tmp_endpoint_path,
        '-abs', '0.1',
        output_mask_path
    ]

    # 执行命令
    try:
        subprocess.run(cmd1, check=True)
        subprocess.run(cmd2, check=True)
    finally:
        if os.path.exists(tmp_endpoint_path):
            os.remove(tmp_endpoint_path)

