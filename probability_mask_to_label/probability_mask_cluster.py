"""
    coding: utf-8
    Project: Fiber_Query
    File: probability_mask_cluster.py
    Author: xieyu
    Date: 2025/10/15 11:09
    IDE: PyCharm
"""
import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import numpy as np
import nibabel as nib
from tqdm import tqdm

from scipy.ndimage import gaussian_filter

from sklearn.cluster import KMeans, MiniBatchKMeans


def main():

    n_cluster = 100

    in_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/end_points_multi_mask_plus_filtered_norm.nii.gz"
    out_path = f"/media/UG3/xieyu/fiber_query/HCP/HCP_multi_mask_reg_plus/end_points_multi_mask_cluster_{n_cluster}.nii.gz"

    threshold = 0.15

    origin_image_nii = nib.load(in_path)

    origin_image = origin_image_nii.get_fdata()

    smoothed = np.zeros_like(origin_image)
    for i in range(origin_image.shape[-1]):
        smoothed[..., i] = gaussian_filter(origin_image[..., i], sigma=1.0)

    print("smooth over")

    # smoothed[smoothed < threshold] = 0

    smoothed_cp = smoothed.copy()

    smoothed_cp[smoothed_cp < threshold] = 0

    mask = np.any(smoothed_cp != 0, axis=-1)

    # 2. 提取这些体素的特征
    nonzero_voxels = smoothed[mask]  # shape = (N_nonzero, C)

    # 3. 聚类（例如 K=5）
    # kmeans = KMeans(n_clusters=200, random_state=0)

    kmeans = MiniBatchKMeans(
            n_clusters=n_cluster,
            batch_size=10000,
            n_init='auto',
            random_state=0
        )

    labels_nonzero = kmeans.fit_predict(nonzero_voxels)

    # 4. 将聚类结果还原回三维空间
    labels_3d = np.zeros(mask.shape, dtype=np.uint8)
    labels_3d[mask] = labels_nonzero + 49

    new_image_nii = nib.Nifti1Image(labels_3d, affine=origin_image_nii.affine)
    nib.save(new_image_nii, out_path)


if __name__ == '__main__':
    main()
