"""
    coding: utf-8
    Project: Fiber_Query
    File: multi_score_count.py
    Author: xieyu
    Date: 2025/10/20 10:30
    IDE: PyCharm
"""

import os

import numpy as np
from tqdm import tqdm

from utils import write_dict_2_json, read_json

import pandas as pd


def main():

    score_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    subjects = os.listdir(score_base_path)

    methods = ['fiber_query', 'fss_10k', 'reco_bundle_10k', 'ssn']

    all_results = {}

    for method in tqdm(methods):

        micro_precision = []
        micro_recall = []
        micro_f1 = []
        macro_precision = []
        macro_recall = []
        macro_f1 = []

        weighted_precision = []
        weighted_recall = []
        weighted_f1 = []

        samples_precision = []
        samples_recall = []
        samples_f1 = []

        acc_score = []
        HammingLoss = []
        IoU = []
        ROC_AUC = []

        per_class_precision = []

        for subject in tqdm(subjects):
            cur_json_path = os.path.join(score_base_path, subject, f"{method}_metrics.json")
            if not os.path.exists(cur_json_path):
                continue
            print(subject)
            cur_dict = read_json(cur_json_path)
            micro_precision.append(cur_dict['micro-avg']['precision'])
            micro_recall.append(cur_dict['micro-avg']['recall'])
            micro_f1.append(cur_dict['micro-avg']['f1'])
            macro_precision.append(cur_dict['macro-avg']['precision'])
            macro_recall.append(cur_dict['macro-avg']['recall'])
            macro_f1.append(cur_dict['macro-avg']['f1'])
            weighted_precision.append(cur_dict['weighted-avg']['precision'])
            weighted_recall.append(cur_dict['weighted-avg']['recall'])
            weighted_f1.append(cur_dict['weighted-avg']['f1'])
            samples_precision.append(cur_dict['samples-avg']['precision'])
            samples_recall.append(cur_dict['samples-avg']['recall'])
            samples_f1.append(cur_dict['samples-avg']['f1'])
            acc_score.append(cur_dict['acc-score'])
            HammingLoss.append(cur_dict['Hamming-loss'])
            IoU.append(cur_dict['IoU'])
            ROC_AUC.append(cur_dict['ROC-AUC'])
            # print(cur_dict['ROC-AUC'])
            # per_class_precision.append(np.array(cur_dict['per_class_metrics']['precision']))

        ROC_AUC = [x for x in ROC_AUC if x is not None]

        metrics_summary = {
            "micro-avg precision": f"{np.mean(micro_precision):.4f} ± {np.std(micro_precision):.4f}",
            "micro-avg recall": f"{np.mean(micro_recall):.4f} ± {np.std(micro_recall):.4f}",
            "micro-avg f1": f"{np.mean(micro_f1):.4f} ± {np.std(micro_f1):.4f}",
            "macro-avg precision": f"{np.mean(macro_precision):.4f} ± {np.std(macro_precision):.4f}",
            "macro-avg recall": f"{np.mean(macro_recall):.4f} ± {np.std(macro_recall):.4f}",
            "macro-avg f1": f"{np.mean(macro_f1):.4f} ± {np.std(macro_f1):.4f}",
            "weighted-avg precision": f"{np.mean(weighted_precision):.4f} ± {np.std(weighted_precision):.4f}",
            "weighted-avg recall": f"{np.mean(weighted_recall):.4f} ± {np.std(weighted_recall):.4f}",
            "weighted-avg f1": f"{np.mean(weighted_f1):.4f} ± {np.std(weighted_f1):.4f}",
            "samples-avg precision": f"{np.mean(samples_precision):.4f} ± {np.std(samples_precision):.4f}",
            "samples-avg recall": f"{np.mean(samples_recall):.4f} ± {np.std(samples_recall):.4f}",
            "samples-avg f1": f"{np.mean(samples_f1):.4f} ± {np.std(samples_f1):.4f}",
            "acc-score": f"{np.mean(acc_score):.4f} ± {np.std(acc_score):.4f}",
            "Hamming-loss": f"{np.mean(HammingLoss):.4f} ± {np.std(HammingLoss):.4f}",
            "IoU": f"{np.mean(IoU):.4f} ± {np.std(IoU):.4f}",
            "ROC-AUC": f"{np.mean(ROC_AUC):.4f} ± {np.std(ROC_AUC):.4f}" if len(ROC_AUC) > 0 else "N/A",
        }

        all_results[method] = metrics_summary

        # print("micro-avg precision: ", np.mean(micro_precision), np.std(micro_precision))
        # print("micro-avg recall: ", np.mean(micro_recall), np.std(micro_recall))
        # print("micro-avg f1: ", np.mean(micro_f1), np.std(micro_f1))
        # print("macro-avg precision: ", np.mean(macro_precision), np.std(macro_precision))
        # print("macro-avg recall: ", np.mean(macro_recall), np.std(macro_recall))
        # print("macro-avg f1: ", np.mean(macro_f1), np.std(macro_f1))
        # print("weighted-avg precision: ", np.mean(weighted_precision), np.std(weighted_precision))
        # print("weighted-avg recall: ", np.mean(weighted_recall), np.std(weighted_recall))
        # print("weighted-avg f1: ", np.mean(weighted_f1), np.std(weighted_f1))
        # print("samples-avg precision: ", np.mean(samples_precision), np.std(samples_precision))
        # print("samples-avg recall: ", np.mean(samples_recall), np.std(samples_recall))
        # print("samples-avg f1: ", np.mean(samples_f1), np.std(samples_f1))
        # print("acc-score: ", np.mean(acc_score), np.std(acc_score))
        # print("Hamming-loss: ", np.mean(HammingLoss), np.std(HammingLoss))
        # print("IoU: ", np.mean(IoU), np.std(IoU))
        # # print("ROC-AUC: ", np.mean(ROC_AUC), np.std(ROC_AUC))
        # per_class_precision = np.array(per_class_precision)
        # print("per_class_precision: ", np.mean(per_class_precision, axis=0), np.std(per_class_precision, axis=0))

    df = pd.DataFrame(all_results)
    df.index.name = "Metrics"

    # 保存到 Excel
    out_path = os.path.join(score_base_path, "/media/UG3/xieyu/fiber_query/HCP/metrics_summary.xlsx")
    df.to_excel(out_path)


    pass


if __name__ == '__main__':
    main()
