"""
    coding: utf-8
    Project: Fiber_Query
    File: labels_to_tck.py
    Author: xieyu
    Date: 2025/9/15 11:15
    IDE: PyCharm
"""

import os
import glob
import random

import numpy as np
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.io.stateful_tractogram import StatefulTractogram, Space
import nibabel as nib
from tqdm import tqdm

from utils import get_bundle_names


def labels_to_tck(whole_brain_sft, ref_img, labels, bundle_names, out_dir):

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    whole_brain_lines = whole_brain_sft.streamlines

    for i, bundle_name in tqdm(enumerate(bundle_names)):
        if os.path.exists(os.path.join(out_dir, f"{bundle_name}.tck")):
            continue
        cur_labels = labels[:, i]
        cur_indices = np.argwhere(cur_labels == 1).reshape(-1)
        cur_lines = [whole_brain_lines[item] for item in cur_indices]
        cur_sft = StatefulTractogram(cur_lines, reference=ref_img, space=whole_brain_sft.space)

        save_tractogram(cur_sft, os.path.join(out_dir, f"{bundle_name}.tck"), bbox_valid_check=False)

    pass


def main():

    # tck_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"
    # out_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"
    # ref_base_dir = "/media/UG3/xieyu/fiber_query/HCP/T1_un_reg/"
    # ref_file_name = "T1w_acpc_dc_restore_brain.nii.gz"

    tck_base_path = "/media/UG3/xieyu/fiber_query/HCPA/tracking_results/"
    out_base_path = "/media/UG3/xieyu/fiber_query/HCPA/fiber_recognize_results/"
    ref_base_dir = "/media/UG3/xieyu/fiber_query/HCPA/T1_un_reg/"
    ref_file_name = "T1w_acpc_dc_restore_brain.nii.gz"
    # ref_file_name = "t1w.nii.gz"

    bundle_names = get_bundle_names()
    sample_names = os.listdir(tck_base_path)

    # sample_names = ["preop_sub-PAT05"]

    # method = "fiber_query"
    # method = "fss_10k"
    # method = "reco_bundle_10k"
    method = "ssn"

    # sample_names = ['8724991']
    tracking_types = [
        # 'track_ifod2_rk4_wmgmi_1M_step_30',
        'track_ifod1_rk4_dynamic_1M',
        # 'track_ifod1_rk4_seed_1M',
        # 'track_ifod1_rk4_dynamic_1M_step_30',
        # 'track_ifod1_rk4_seed_1M_step_30',
        # 'track_ifod1_rk4_wmgmi_1M',
        # 'track_ifod1_rk4_wmgmi_1M_step_30',
        # 'track_ifod2_rk4_wmgmi_1M',
        # 'track'
    ]

    for sample_name in tqdm(sample_names):
        print(sample_name)

        for tracking_type in tqdm(tracking_types):
            if not os.path.exists(os.path.join(out_base_path, sample_name, f"{method}_labels-{tracking_type}.npy")):
                continue

            cur_whole_brain_path = os.path.join(tck_base_path, sample_name, f"{tracking_type}.tck")

            cur_ref_path = os.path.join(ref_base_dir, sample_name, ref_file_name)
            cur_ref = nib.load(cur_ref_path)

            cur_whole_brain_sft = load_tractogram(cur_whole_brain_path, reference=cur_ref, bbox_valid_check=False)

            cur_labels = np.load(os.path.join(out_base_path, sample_name, f"{method}_labels-{tracking_type}.npy")).astype(int)

            labels_to_tck(cur_whole_brain_sft, cur_ref, cur_labels, bundle_names,
                          os.path.join(out_base_path, sample_name, f"{method}_results-{tracking_type}"))

    pass


if __name__ == '__main__':
    main()


