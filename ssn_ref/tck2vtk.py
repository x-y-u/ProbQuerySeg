"""
    coding: utf-8
    Project: Fiber_Query
    File: tck2vtk.py
    Author: xieyu
    Date: 2025/10/17 10:01
    IDE: PyCharm
"""
import os
from dipy.io.streamline import load_tractogram, save_tractogram


def tck_to_vtk_dipy(tck_path, references, vtk_path=None):
    tck = load_tractogram(tck_path, reference=references, bbox_valid_check=False)
    save_tractogram(tck, vtk_path, bbox_valid_check=False)


def main():

    # tck_base_dir = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"
    #
    # out_base_dir = "/media/UG3/xieyu/fiber_query/ref_test/HCP_whole_brain_vtk"
    # if not os.path.exists(out_base_dir):
    #     os.makedirs(out_base_dir)
    # ref_base_dir = "/media/UG3/xieyu/fiber_query/HCP/T1_un_reg/"


    tck_base_dir = "/media/UG3/xieyu/fiber_query/HCPA/tracking_results/"

    out_base_dir = "/media/UG3/xieyu/fiber_query/HCPA/tracking_results_vtk/"

    if not os.path.exists(out_base_dir):
        os.makedirs(out_base_dir)
    ref_base_dir = "/media/UG3/xieyu/fiber_query/HCPA/T1_un_reg/"

    subjects = os.listdir(tck_base_dir)

    subjects = [
        # 'preop_sub-PAT08',
        # 'preop_sub-PAT26',
        # 'postop_sub-CON02'

        '6086369'
    ]

    for subject in subjects:
        cur_tck_path = os.path.join(tck_base_dir, subject, "track_ifod1_rk4_dynamic_1M.tck")
        cur_out_path = os.path.join(out_base_dir, f"{subject}.vtk")
        cur_ref_path = os.path.join(ref_base_dir, subject, "T1w_acpc_dc_restore_brain.nii.gz")
        tck_to_vtk_dipy(cur_tck_path, cur_ref_path, cur_out_path)


if __name__ == '__main__':
    main()
