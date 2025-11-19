"""
    coding: utf-8
    Project: Fiber_Query
    File: multi_sub_class_count.py
    Author: xieyu
    Date: 2025/10/23 14:34
    IDE: PyCharm
"""


import os

import numpy as np
from tqdm import tqdm

from utils import write_dict_2_json, read_json, get_bundle_names
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def compute_metrics_from_confusion(tp, fp, fn):
    """根据 TP, FP, FN 计算 overlap, overlap_vs, precision, f1"""
    eps = 1e-8  # 防止除零

    precision = tp / (tp + fp + eps)
    recall = tp / (tp + fn + eps)
    f1 = 2 * tp / (2 * tp + fp + fn + eps)
    overlap = tp / (tp + fp + fn + eps)
    overreach_vs = fp / (tp + fp + eps)

    result = {
        "overlap": round(overlap, 4),
        "overreach_vs": round(overreach_vs, 4),
        "precision": round(precision, 4),
        "f1": round(f1, 4),
    }
    return result


def main():
    score_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    subjects = os.listdir(score_base_path)

    methods = ['fiber_query', 'ssn', 'fss_10k', 'reco_bundle_10k']

    method_names = ['Fiber_Query', 'Transformer', 'FastStreamlineSearch', 'Reco_Bundle']

    sub_classes = {
        'association':[
            'AF_left', 'AF_right', 'CG_left', 'CG_right', 'ILF_left', 'ILF_right',
            'MLF_left', 'MLF_right', 'UF_left', 'UF_right', 'IFO_left', 'IFO_right',
            'SLF_I_left', 'SLF_I_right', 'SLF_II_left', 'SLF_II_right', 'SLF_III_left', 'SLF_III_right',

        ],
        'projection':[
            'CST_left', 'CST_right', 'FPT_left', 'FPT_right', 'POPT_left', 'POPT_right', 'FX_left', 'FX_right',
            'STR_left', 'STR_right','T_PREF_left', 'T_PREF_right', 'T_PREM_left',
           'T_PREM_right', 'T_PREC_left', 'T_PREC_right', 'T_POSTC_left', 'T_POSTC_right', 'T_PAR_left',
           'T_PAR_right', 'T_OCC_left', 'T_OCC_right', 'ST_FO_left', 'ST_FO_right', 'ST_PREF_left',
           'ST_PREF_right', 'ST_PREM_left', 'ST_PREM_right', 'ST_PREC_left', 'ST_PREC_right', 'ST_POSTC_left',
           'ST_POSTC_right', 'ST_PAR_left', 'ST_PAR_right', 'ST_OCC_left', 'ST_OCC_right',
            'OR_left', 'OR_right'
        ],
        'cerebellum':[
            'ATR_left', 'ATR_right', 'ICP_left', 'ICP_right', 'MCP', 'SCP_left', 'SCP_right'
        ],
        'commissural':[
            'CA', 'CC_1', 'CC_2', 'CC_3', 'CC_4', 'CC_5', 'CC_6', 'CC_7', 'CC'
        ],

    }

    inverse_dict = {sub: cls for cls, subs in sub_classes.items() for sub in subs}

    bundle_names = get_bundle_names()

    metrics_sub_class = ['overlap', 'overreach_vs', 'precision', 'f1']
    metrics = ['tp', 'fp', 'fn']

    records = {}

    for method in methods:
        records[method] = {}
        for sub_class in sub_classes.keys():
            for metric in metrics:
                records[method][f"{sub_class}-{metric}"] = {}
                for subject in subjects:
                    records[method][f"{sub_class}-{metric}"][subject] = 0

    for i, method in tqdm(enumerate(methods)):
        for subject in tqdm(subjects):
            cur_json_path = os.path.join(score_base_path, subject, f"{method}_metrics.json")
            if not os.path.exists(cur_json_path):
                continue

            cur_dict = read_json(cur_json_path)

            # for class_id, bundle_name in enumerate(bundle_names):
            #
            #     for metric in metrics:
            #         # records[method][f"{inverse_dict[bundle_name]}-{metric}"].append(cur_dict[bundle_name][metric])
            #         records[method][f"{inverse_dict[bundle_name]}-{metric}"][subject] += cur_dict[bundle_name][metric]

            precision, recall, support = (np.array(cur_dict['per_class_metrics']['precision']), np.array(cur_dict['per_class_metrics']['recall']),
                                              np.array(cur_dict['per_class_metrics']['support']))
            TP = recall * support
            FP = np.where(precision > 0, TP * (1 / precision - 1), 0)
            FN = support - TP

            for class_id, bundle_name in enumerate(bundle_names):
                records[method][f"{inverse_dict[bundle_name]}-tp"][subject] += TP[class_id]
                records[method][f"{inverse_dict[bundle_name]}-fp"][subject] += FP[class_id]
                records[method][f"{inverse_dict[bundle_name]}-fn"][subject] += FN[class_id]

    records_sub_class = {}

    for method in methods:
        records_sub_class[method] = {}
        for sub_class in sub_classes.keys():
            for metric in metrics_sub_class:
                records_sub_class[method][f"{sub_class}-{metric}"] = []
            for subject in subjects:

                tp, fp, fn = records[method][f"{sub_class}-tp"][subject], records[method][f"{sub_class}-fp"][subject], records[method][f"{sub_class}-fn"][subject]

                cur_metrics = compute_metrics_from_confusion(tp, fp, fn)
                # print(cur_metrics)

                for metric in metrics_sub_class:
                    records_sub_class[method][f"{sub_class}-{metric}"].append(cur_metrics[metric])

    results = []
    for method, metrics_dict in records_sub_class.items():
        row = {"Method": method}
        for key, values in metrics_dict.items():
            if len(values) == 0:
                val_str = "-"
            else:
                mean_val = np.mean(values)
                std_val = np.std(values)
                val_str = f"{mean_val:.4f} ± {std_val:.4f}"
            row[key] = val_str
        results.append(row)

    # 转为DataFrame
    df = pd.DataFrame(results)

    # 保存为Excel
    out_path = os.path.join(score_base_path, "/media/UG3/xieyu/fiber_query/HCP/sub_class_summary.xlsx")
    df.to_excel(out_path, index=False)
    print(f"✅ 已保存结果到 {out_path}")


if __name__ == '__main__':
    main()
