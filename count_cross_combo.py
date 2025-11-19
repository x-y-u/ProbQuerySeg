"""
    coding: utf-8
    Project: Fiber_Query
    File: count_cross_combo.py
    Author: xieyu
    Date: 2025/8/12 21:00
    IDE: PyCharm
"""

import os

import nibabel as nib

from tqdm import tqdm
from utils import read_connection_dicts, get_bundle_names


def main():

    combo_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_connection_pair/"

    sample_names = os.listdir(combo_base_path)

    bundle_names = get_bundle_names()

    for sample_name in tqdm(sample_names):
        cur_base_path = os.path.join(combo_base_path, sample_name)

        cur_set = set()

        repeat_set = set()

        repeated_count = 0

        for bundle_name in tqdm(bundle_names):
            cur_path = os.path.join(cur_base_path, f"{bundle_name}.txt")
            cur_dict = read_connection_dicts(cur_path)
            for key in cur_dict.keys():
                if key in cur_set:
                    repeated_count += 1
                    repeat_set.add(key)
                else:
                    cur_set.add(key)
        print(sample_name, repeated_count, len(cur_set), len(repeat_set))


    pass


if __name__ == '__main__':
    main()


