"""
    coding: utf-8
    Project: Fiber_Query
    File: generate_label_transform.py
    Author: xieyu
    Date: 2025/9/8 10:11
    IDE: PyCharm
"""

import nibabel as nib
import numpy as np
from tqdm import tqdm

from utils import write_dict_2_json


def main():

    label_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_reg_plus/end_points_multi_mask_label.nii.gz"
    multi_mask_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_reg_plus/end_points_multi_mask_plus_filtered_norm.nii.gz"
    out_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_reg_plus/end_points_multi_mask_label_transform.json"
    threshold = 0.1

    label = nib.load(label_path).get_fdata().astype(int)
    multi_mask = nib.load(multi_mask_path).get_fdata()

    multi_mask = multi_mask > threshold

    unique_labels = np.unique(label)

    results = dict()

    for unique_label in tqdm(unique_labels):
        if unique_label == 0:
            continue
        indices = np.argwhere(label == unique_label)

        x, y, z = indices[:, 0], indices[:, 1], indices[:, 2]

        cur_mask = multi_mask[x, y, z]

        cur_mask = np.mean(cur_mask, axis=0)

        results[f"{unique_label}"] = list(cur_mask)

        # print(unique_label, cur_mask)


    write_dict_2_json(results, out_path)


if __name__ == '__main__':
    main()
