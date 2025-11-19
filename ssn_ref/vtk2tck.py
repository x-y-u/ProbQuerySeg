"""
    coding: utf-8
    Project: Fiber_Query
    File: vtk2tck.py
    Author: xieyu
    Date: 2025/10/17 11:54
    IDE: PyCharm
"""

import os
from dipy.io.streamline import load_tractogram, save_tractogram
from tqdm import tqdm


def tck_to_vtk_dipy(tck_path, references, vtk_path=None):
    tck = load_tractogram(tck_path, reference=references, bbox_valid_check=False)
    save_tractogram(tck, vtk_path, bbox_valid_check=False)


def trk_to_tck_dipy(trk_path, tck_path=None):
    sft = load_tractogram(trk_path, reference="same", bbox_valid_check=False)
    save_tractogram(sft, tck_path, bbox_valid_check=False)


def main():

    tck_base_dir = "/media/UG3/xieyu/fiber_query/ref_test/ssn_inf_results/"

    out_base_dir = "/media/UG3/xieyu/fiber_query/ref_test/ssn_inf_results_tck/"
    if not os.path.exists(out_base_dir):
        os.makedirs(out_base_dir)
    ref_base_dir = "/media/UG3/xieyu/fiber_query/HCP/T1_un_reg/"

    for tck in tqdm(os.listdir(tck_base_dir)):
        bundle_name = tck.split(".")[0]
        if not tck.endswith(".vtk"):
            continue
        cur_tck_path = os.path.join(tck_base_dir, f"{bundle_name}.vtk")
        cur_out_path = os.path.join(out_base_dir, f"{bundle_name}.tck")
        cur_ref_path = os.path.join(ref_base_dir, "896879", "T1w_acpc_dc_restore_brain.nii.gz")
        tck_to_vtk_dipy(cur_tck_path, cur_ref_path, cur_out_path)


if __name__ == '__main__':
    main()
