"""
    coding: utf-8
    Project: Fiber_Query
    File: HCP_test1.py
    Author: xieyu
    Date: 2025/10/17 10:54
    IDE: PyCharm
"""


"""
Dice score

Overlap ratio (OL, OR)

Volume difference
"""

import numpy as np

from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    classification_report, confusion_matrix
)

import pandas as pd


def main():

    methods = [
        "reco_bundle_10k",
        "fss_10k",
        "fiber_query"
    ]

    pred_path = f"/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/826454/{methods[0]}_labels.npy"

    gt_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/826454/labels.npy"

    pred_probs = np.load(pred_path)
    y_true = np.load(gt_path)

    y_pred = np.argmax(pred_probs, axis=1)

    acc = accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average='macro')
    f1_micro = f1_score(y_true, y_pred, average='micro')
    f1_weighted = f1_score(y_true, y_pred, average='weighted')
    precision_macro = precision_score(y_true, y_pred, average='macro')
    recall_macro = recall_score(y_true, y_pred, average='macro')

    print("✅ Overall metrics:")
    print(f"Accuracy: {acc:.4f}")
    print(f"F1 (macro): {f1_macro:.4f}")
    print(f"F1 (micro): {f1_micro:.4f}")
    print(f"F1 (weighted): {f1_weighted:.4f}")
    print(f"Precision (macro): {precision_macro:.4f}")
    print(f"Recall (macro): {recall_macro:.4f}")

    report = classification_report(y_true, y_pred, output_dict=True)

    df_report = pd.DataFrame(report).transpose()
    print(df_report)


if __name__ == '__main__':
    main()
