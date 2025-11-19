"""
    coding: utf-8
    Project: Fiber_Query
    File: generate_combo_max_probability.py
    Author: xieyu
    Date: 2025/8/14 11:35
    IDE: PyCharm
"""

import os

import nibabel as nib

from tqdm import tqdm
from utils import read_connection_dicts, get_bundle_names, write_connection_dicts


def main():
    combo_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_connection_pair/"

    out_base_path = "/media/UG3/xieyu/tractography_generate/HCP/HCP_max_probability_pair/"
    if not os.path.exists(out_base_path):
        os.makedirs(out_base_path)

    sample_names = os.listdir(combo_base_path)

    bundle_names = get_bundle_names()

    for bundle_name in tqdm(bundle_names):

        all_dicts = dict()
        cur_out_path = os.path.join(out_base_path, f"{bundle_name}.txt")

        for sample_name in tqdm(sample_names):
            cur_path = os.path.join(combo_base_path, sample_name, f"{bundle_name}.txt")

            cur_dict = read_connection_dicts(cur_path, get_probability=True)

            for key in cur_dict.keys():
                if key not in all_dicts:
                    all_dicts[key] = cur_dict[key]
                elif cur_dict[key] > all_dicts[key]:
                    all_dicts[key] = cur_dict[key]
                else:
                    continue

        write_connection_dicts(all_dicts, cur_out_path)

    pass


if __name__ == '__main__':
    main()
