"""
    coding: utf-8
    Project: Fiber_Query
    File: merge_whole_brain_bundles.py
    Author: xieyu
    Date: 2025/9/12 15:41
    IDE: PyCharm
"""
import numpy as np
from dipy.io.streamline import load_tractogram, save_tractogram, Space, StatefulTractogram
import os

from tqdm import tqdm

from utils import get_bundle_names


def main():

    data_base_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_tracts_tck/"
    bundle_names = get_bundle_names()
    references_base_path = "/media/UG3/xieyu/fiber_query/HCP/T1_un_reg/"

    out_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    for subject in tqdm(os.listdir(data_base_path)):
        cur_base_path = os.path.join(data_base_path, subject, "tracts")

        cur_reference_path = os.path.join(references_base_path, subject, "T1w_acpc_dc_restore_brain.nii.gz")

        cur_out_base_path = os.path.join(out_base_path, subject)

        if not os.path.exists(cur_out_base_path):
            os.makedirs(cur_out_base_path)

        whole_brain_lines = []

        labels = []

        for i, bundle in enumerate(bundle_names):
            cur_bundle_path = os.path.join(cur_base_path, f"{bundle}.tck")
            if not os.path.exists(cur_bundle_path):
                continue

            cur_sft = load_tractogram(cur_bundle_path, reference=cur_reference_path, bbox_valid_check=False)
            cur_bundle = cur_sft.streamlines

            whole_brain_lines.extend(cur_bundle)

            labels.extend([i] * len(cur_bundle))

        new_sft = StatefulTractogram(whole_brain_lines, reference=cur_reference_path, space=cur_sft.space)

        save_tractogram(new_sft, os.path.join(cur_out_base_path, f"whole_brain.tck"), bbox_valid_check=False)

        np.save(os.path.join(cur_out_base_path, f"labels.npy"), np.array(labels))


if __name__ == '__main__':
    main()
