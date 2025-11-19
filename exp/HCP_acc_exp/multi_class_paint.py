"""
    coding: utf-8
    Project: Fiber_Query
    File: multi_class_paint.py
    Author: xieyu
    Date: 2025/10/21 17:59
    IDE: PyCharm
"""

import os

import numpy as np
from tqdm import tqdm

from utils import write_dict_2_json, read_json, get_bundle_names
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def main():
    score_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    subjects = os.listdir(score_base_path)

    methods = ['fiber_query', 'ssn', 'fss_10k', 'reco_bundle_10k']

    method_names = ['ProbQuerySeg', 'Transformer', 'FastStreamlineSearch', 'Reco_Bundle']

    palette = {
        'ProbQuerySeg': '#df2020',  # 红色
        'Transformer': '#4de5e5',  # 蓝色
        'FastStreamlineSearch': '#e5e54d',  # 橙色
        'Reco_Bundle': '#4de573',  # 绿色
    }

    bundle_names = get_bundle_names()

    # records = []
    #
    # low_metric = "precision"
    # high_metric = "Precision"
    #
    # for i, method in tqdm(enumerate(methods)):
    #     for subject in tqdm(subjects):
    #         cur_json_path = os.path.join(score_base_path, subject, f"{method}_metrics.json")
    #         if not os.path.exists(cur_json_path):
    #             continue
    #
    #         cur_dict = read_json(cur_json_path)
    #         per_class_value = np.array(cur_dict['per_class_metrics'][low_metric])
    #
    #         for class_id, cur_value in enumerate(per_class_value):
    #             records.append({
    #                 'method': method_names[i],
    #                 'bundle_name': bundle_names[class_id],
    #                 low_metric: cur_value
    #             })
    #
    # # 转为DataFrame
    # df = pd.DataFrame(records)

    # plt.subplots(facecolor='white')
    #
    # plt.figure(figsize=(60, 20))
    #
    # plt.xticks(rotation=55, ha='right', fontsize=20)
    #
    # plt.yticks(fontsize=16)
    #
    # ax = sns.boxplot(x='bundle_name', y=low_metric, hue='method', data=df, showfliers=False, palette=palette, linewidth=2.0)
    #
    # for spine in ax.spines.values():
    #     spine.set_linewidth(2.0)
    #
    # plt.title(f'Per-Class {high_metric} Comparison', fontsize=24, fontweight='bold')
    # plt.ylabel(f'{high_metric} Score', fontsize=22, fontweight='bold')
    # plt.xlabel('Bundle Name', fontsize=22, fontweight='bold')
    # plt.legend(title='Method', loc='lower left', fontsize=24, title_fontsize=24)
    # plt.tight_layout()
    #
    # out_path = f"/media/UG3/xieyu/fiber_query/HCP/per_class_{low_metric}.png"
    #
    # # plt.show()
    #
    # plt.savefig(out_path, dpi=500, transparent=False, facecolor='white')
    #
    # pass

    # summary = (
    #     df.groupby(['bundle_name', 'method'])[low_metric]
    #     .agg(['mean', 'std'])
    #     .reset_index()
    # )
    #
    # bundle_names = summary['bundle_name'].unique()
    #
    # plt.figure(figsize=(60, 15), facecolor='white')
    # ax = plt.gca()
    #
    # # 对每个 method 分别绘制折线及方差阴影
    # for i, method in enumerate(method_names):
    #     sub_df = summary[summary['method'] == method]
    #     x = np.arange(len(sub_df))
    #     y = sub_df['mean']
    #     yerr = sub_df['std']
    #
    #     # 绘制折线
    #     ax.plot(x, y, label=method, color=palette[method], linewidth=3)
    #
    #     # 绘制方差阴影
    #     ax.fill_between(x, y - yerr, y + yerr, color=palette[method], alpha=0.2)
    #
    # # 边框加粗
    # for spine in ax.spines.values():
    #     spine.set_linewidth(2.0)
    #
    # plt.xticks(rotation=55, ha='right', fontsize=20)
    # plt.yticks(fontsize=19, fontweight='bold')
    # plt.title(f'Per-Class {high_metric} Comparison', fontsize=24, fontweight='bold')
    # plt.ylabel(f'{high_metric} Score', fontsize=25, fontweight='bold')
    # plt.xlabel('Bundle Name', fontsize=25, fontweight='bold')
    # plt.legend(title='Method', loc='lower left', fontsize=24, title_fontsize=27)
    #
    # ax.set_xticks(np.arange(len(bundle_names)))
    # ax.set_xticklabels(bundle_names, rotation=55, ha='right', fontsize=22, fontweight='bold')
    #
    # ax.margins(x=0)
    #
    # plt.tight_layout()
    #
    # # ====== 保存 ======
    # out_path = f"/media/UG3/xieyu/fiber_query/HCP/per_class_{high_metric}_line.png"
    # # plt.show()
    # plt.savefig(out_path, dpi=500, bbox_inches='tight', pad_inches=0, facecolor='white')
    # plt.close()


    records = []

    low_metric = "overreach_vs"
    high_metric = "Volume_OR"

    for i, method in tqdm(enumerate(methods)):
        for subject in tqdm(subjects):
            cur_json_path = os.path.join(score_base_path, subject, f"{method}_volumn_metrics.json")
            if not os.path.exists(cur_json_path):
                continue

            cur_dict = read_json(cur_json_path)

            for class_id, bundle_name in enumerate(bundle_names):
                records.append({
                    'method': method_names[i],
                    'bundle_name': bundle_name,
                    low_metric: cur_dict[bundle_name][low_metric]
                })

    # print(len(records))

    # 转为DataFrame
    df = pd.DataFrame(records)

    # plt.subplots(facecolor='white')
    #
    # plt.figure(figsize=(60, 20))
    #
    # ax = sns.boxplot(x='bundle_name', y=low_metric, hue='method', data=df, showfliers=False, palette=palette,
    #                  linewidth=2.0)
    #
    # for spine in ax.spines.values():
    #     spine.set_linewidth(2.0)
    #
    # plt.xticks(rotation=55, ha='right', fontsize=20)
    # plt.yticks(fontsize=16)
    # plt.title(f'Per-Class {high_metric} Comparison', fontsize=24, fontweight='bold')
    # plt.ylabel(f'{high_metric} Score', fontsize=22, fontweight='bold')
    # plt.xlabel('Bundle Name', fontsize=22, fontweight='bold')
    # plt.legend(title='Method', loc='upper left', fontsize=24, title_fontsize=24)
    # plt.tight_layout()
    #
    # out_path = f"/media/UG3/xieyu/fiber_query/HCP/per_class_{high_metric}.png"
    #
    # # plt.show()
    #
    # plt.savefig(out_path, dpi=500, transparent=False, facecolor='white')
    #
    # pass

    summary = (
        df.groupby(['bundle_name', 'method'])[low_metric]
        .agg(['mean', 'std'])
        .reset_index()
    )

    bundle_names = summary['bundle_name'].unique()

    plt.figure(figsize=(60, 9), facecolor='white')
    ax = plt.gca()

    # 对每个 method 分别绘制折线及方差阴影
    for i, method in enumerate(method_names):
        sub_df = summary[summary['method'] == method]
        x = np.arange(len(sub_df))
        y = sub_df['mean']
        yerr = sub_df['std']

        # 绘制折线
        ax.plot(x, y, label=method, color=palette[method], linewidth=3)

        # 绘制方差阴影
        ax.fill_between(x, y - yerr, y + yerr, color=palette[method], alpha=0.2)

    # 边框加粗
    for spine in ax.spines.values():
        spine.set_linewidth(2.0)

    plt.xticks(rotation=55, ha='right', fontsize=22)
    plt.yticks(fontsize=21, fontweight='bold')
    plt.title(f'Per-Class {high_metric} Comparison', fontsize=25, fontweight='bold')
    plt.ylabel(f'{high_metric} Score', fontsize=25, fontweight='bold')
    # plt.xlabel('Bundle Name', fontsize=25, fontweight='bold')
    plt.legend(title='Method', loc='upper left', fontsize=24, title_fontsize=27)

    ax.set_xticks(np.arange(len(bundle_names)))
    ax.set_xticklabels(bundle_names, rotation=55, ha='right', fontsize=22, fontweight='bold')

    ax.margins(x=0)

    plt.tight_layout()

    # ====== 保存 ======
    out_path = f"/media/UG3/xieyu/fiber_query/HCP/per_class_{high_metric}_line.svg"
    # plt.show()
    plt.savefig(out_path, dpi=500, bbox_inches='tight', pad_inches=0, facecolor='white')
    plt.close()


if __name__ == '__main__':
    main()
