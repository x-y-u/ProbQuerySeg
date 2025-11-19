"""
    coding: utf-8
    Project: Fiber_Query
    File: BTC_length_paint.py
    Author: xieyu
    Date: 2025/10/16 11:56
    IDE: PyCharm
"""
import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils import get_bundle_names


def main():

    methods = [
        'fiber_query_results-track_ifod1_rk4_dynamic_1M-thined',
        'fss_10k_results-track_ifod1_rk4_dynamic_1M-thined',
        'TractSeg_results',
        'Atlas_tck_in_person'
    ]

    methods_names = [
        'fiber_query',
        'fss',
        'TractSeg',
        'Atlas'
    ]

    base_dir = "/media/UG3/xieyu/fiber_query/BTC/fiber_recognize_results_info/"

    out_base_dir = "/media/UG3/xieyu/fiber_query/BTC/fiber_recognize_results_paint/"

    subjects = os.listdir(base_dir)
    # subjects = ['preop_sub-PAT26']
    bundle_names = get_bundle_names()

    for subject in subjects:
        cur_out_base_dir = os.path.join(out_base_dir, subject)
        if not os.path.exists(cur_out_base_dir):
            os.makedirs(cur_out_base_dir)
        for bundle_name in bundle_names:
            data = {}
            for i, method in enumerate(methods):
                if method == 'Atlas_tck_in_person':
                    if not os.path.exists(os.path.join(base_dir, subject, method, f"{bundle_name}_10k.txt")):
                        continue
                    data[methods_names[i]] = np.loadtxt(os.path.join(base_dir, subject, method, f"{bundle_name}_10k.txt"),
                                                        skiprows=1)
                    continue
                if not os.path.exists(os.path.join(base_dir, subject, method, f"{bundle_name}.txt")):
                    continue
                data[methods_names[i]] = np.loadtxt(os.path.join(base_dir, subject, method, f"{bundle_name}.txt"), skiprows=1)

            # === 绘图 ===
            plt.figure(figsize=(8, 5))
            sns.set(style="whitegrid", font_scale=1.2)

            # 使用 KDE 曲线（平滑的分布曲线），也可以改为 histplot
            for name, lengths in data.items():
                sns.kdeplot(lengths, label=name, linewidth=2)

            plt.xlabel("Fiber Length (mm)")
            plt.ylabel("Density")
            plt.title(f"Length Distribution - {bundle_name}")
            plt.legend(title="Result Type")
            plt.tight_layout()

            # === 保存或展示 ===
            plt.savefig(os.path.join(cur_out_base_dir, f"{bundle_name}.png"), dpi=300)
            plt.close()
            # plt.show()
            # break



if __name__ == '__main__':
    main()
