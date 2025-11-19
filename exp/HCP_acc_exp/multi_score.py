"""
    coding: utf-8
    Project: Fiber_Query
    File: multi_score.py
    Author: xieyu
    Date: 2025/10/17 11:05
    IDE: PyCharm
"""
import os

import numpy as np
from sklearn.metrics import (
    accuracy_score, hamming_loss, precision_score, recall_score, f1_score,
    roc_auc_score, jaccard_score, precision_recall_fscore_support
)
from tqdm import tqdm

from utils import write_dict_2_json, read_json
from sklearn.preprocessing import label_binarize


def compute_multilabel_metrics(y_true_bin, y_pred):
    metrics = {}

    # 🔹 Micro 平均
    metrics["micro-avg"] = {
        "precision": float(precision_score(y_true_bin, y_pred, average='micro', zero_division=0)),
        "recall": float(recall_score(y_true_bin, y_pred, average='micro', zero_division=0)),
        "f1": float(f1_score(y_true_bin, y_pred, average='micro', zero_division=0)),
    }

    # 🔹 Macro 平均
    metrics["macro-avg"] = {
        "precision": float(precision_score(y_true_bin, y_pred, average='macro', zero_division=0)),
        "recall": float(recall_score(y_true_bin, y_pred, average='macro', zero_division=0)),
        "f1": float(f1_score(y_true_bin, y_pred, average='macro', zero_division=0)),
    }

    # 🔹 Weighted 平均
    metrics["weighted-avg"] = {
        "precision": float(precision_score(y_true_bin, y_pred, average='weighted', zero_division=0)),
        "recall": float(recall_score(y_true_bin, y_pred, average='weighted', zero_division=0)),
        "f1": float(f1_score(y_true_bin, y_pred, average='weighted', zero_division=0)),
    }

    # 🔹 Samples 平均
    metrics["samples-avg"] = {
        "precision": float(precision_score(y_true_bin, y_pred, average='samples', zero_division=0)),
        "recall": float(recall_score(y_true_bin, y_pred, average='samples', zero_division=0)),
        "f1": float(f1_score(y_true_bin, y_pred, average='samples', zero_division=0)),
    }

    # 🔹 准确率、Hamming损失、IoU、ROC-AUC
    metrics["acc-score"] = float(accuracy_score(y_true_bin, y_pred))
    metrics["Hamming-loss"] = float(hamming_loss(y_true_bin, y_pred))
    metrics["IoU"] = float(jaccard_score(y_true_bin, y_pred, average='samples', zero_division=0))

    try:
        metrics["ROC-AUC"] = float(roc_auc_score(y_true_bin, y_pred, average='macro'))
    except ValueError:
        metrics["ROC-AUC"] = None

    precision, recall, f1, support = precision_recall_fscore_support(y_true_bin, y_pred, average=None, zero_division=0)

    metrics['per_class_metrics'] = {
        "precision": [float(x) for x in precision],
        "recall": [float(x) for x in recall],
        "f1": [float(x) for x in f1],
        "support": [int(x) for x in support],
    }

    return metrics


def main():
    methods = [
        "reco_bundle_10k",
        # "fss_10k",
        # "fiber_query",
        # "ssn"
    ]

    #
    # metrics = [
    #     'micro-avg',
    #     'macro-avg',
    #     'weighted-avg',
    #     'samples-avg',
    #     'acc-score',
    #     'Hamming-loss',
    #     'precision',
    #     'recall',
    #     'f1-score',
    #     'IoU',
    #     'ROC-AUC',
    #
    # ]
    #
    # per_class_mrtrics = [
    #     'precision',
    #     'recall',
    #     'f1-score',
    # ]

    n_classes = 72
    pred_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"
    # pred_base_path = "/media/UG3/xieyu/fiber_query/ref_test/HCP_SSN_results/"

    gt_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    for subject in tqdm(os.listdir(pred_base_path)):
        cur_gt_path = os.path.join(gt_base_path, subject, "labels.npy")
        y_true = np.load(cur_gt_path)
        y_true_bin = np.zeros((len(y_true), n_classes))
        y_true_bin[np.arange(len(y_true)), y_true] = 1

        for method in tqdm(methods):
            cur_pred_path = os.path.join(pred_base_path, subject, f"{method}_labels.npy")
            cur_out_path = os.path.join(gt_base_path, subject, f"{method}_metrics.json")
            if not os.path.exists(cur_pred_path) or os.path.exists(cur_out_path):
                continue

            y_pred = np.load(cur_pred_path)
            print(f"{subject}-{method}")
            metrics_result = compute_multilabel_metrics(y_true_bin, y_pred)
            write_dict_2_json(metrics_result, cur_out_path)
        #     break
        #
        # break

    pass


if __name__ == '__main__':
    main()
