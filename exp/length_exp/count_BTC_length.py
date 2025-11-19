"""
    coding: utf-8
    Project: Fiber_Query
    File: count_BTC_length.py
    Author: xieyu
    Date: 2025/10/15 17:18
    IDE: PyCharm
"""


import os
import subprocess


def main():

    # base_path = "/media/UG3/xieyu/fiber_query/BTC/fiber_recognize_results/"
    # dir_name = "fss_10k_results-track_ifod1_rk4_dynamic_1M-thined"
    # base_path = "/media/UG3/xieyu/fiber_query/BTC/tractseg_output/"
    # dir_name = "tractseg_output/TOM_trackings"
    base_path = "/media/UG3/xieyu/fiber_query/BTC/fiber_recognize_results/"
    dir_name = "fiber_query_results-track_ifod1_rk4_dynamic_1M-thined"

    out_base_path = "/media/UG3/xieyu/fiber_query/BTC/fiber_recognize_results_info/"

    for subject in os.listdir(base_path):
        tck_base_dir = os.path.join(base_path, subject, dir_name)
        out_base_dir = os.path.join(out_base_path, subject, dir_name)
        # out_base_dir = os.path.join(out_base_path, subject, "TractSeg_results")
        if not os.path.exists(out_base_dir):
            os.makedirs(out_base_dir)
        for tck in os.listdir(tck_base_dir):
            tck_name = tck.split(".")[0]
            tck_path = os.path.join(tck_base_dir, tck)
            out_path = os.path.join(out_base_dir, f"{tck_name}.txt")

            cmd = f"tckstats {tck_path} -dump {out_path} -force"
            subprocess.run(cmd, shell=True, check=True)

    print("✅ All files processed successfully!")

    pass


if __name__ == '__main__':
    main()
