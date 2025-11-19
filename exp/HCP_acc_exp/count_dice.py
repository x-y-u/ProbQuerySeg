"""
    coding: utf-8
    Project: Fiber_Query
    File: count_dice.py
    Author: xieyu
    Date: 2025/10/21 15:07
    IDE: PyCharm
"""
import os

from tqdm import tqdm

from utils import get_bundle_names, write_dict_2_json

import nibabel as nib
import numpy as np


# def get_dice(gt_path, pred_path):
#     gt = nib.load(gt_path).get_fdata().astype(int)
#     pred = np.load(pred_path).get_fdata().astype(int)
#
#     result = {}
#     result['gt_num'] = np.sum(gt)
#     result['pred_num'] = np.sum(pred)
#     intersection = np.sum(gt * pred)
#     result['dice'] = 2.0 * intersection / (np.sum(gt) + np.sum(pred) + 1e-8)
#     return result


def get_metrics(gt_path, pred_path):
    gt = nib.load(gt_path).get_fdata().astype(int)
    pred = nib.load(pred_path).get_fdata().astype(int)

    # 计算 TP, FP, FN
    tp = np.sum((gt == 1) & (pred == 1))
    fp = np.sum((gt == 0) & (pred == 1))
    fn = np.sum((gt == 1) & (pred == 0))

    # 总体数
    gt_num = np.sum(gt)
    pred_num = np.sum(pred)

    # Dice
    dice = 2.0 * tp / (gt_num + pred_num + 1e-8)

    # Overlap (OL)
    overlap = tp / (tp + fn + 1e-8)

    # Overreach normalized by predicted bundle (OR_vs)
    overreach_vs = fp / (tp + fp + 1e-8)

    # Precision & Recall
    precision = tp / (tp + fp + 1e-8)
    recall = tp / (tp + fn + 1e-8)

    # F1
    f1 = 2 * precision * recall / (precision + recall + 1e-8)

    return {
        "gt_num": int(gt_num),
        "pred_num": int(pred_num),
        "tp": int(tp),
        "fp": int(fp),
        "fn": int(fn),
        "dice": float(dice),
        "overlap": float(overlap),
        "overreach_vs": float(overreach_vs),
        "precision": float(precision),
        "f1": float(f1)
    }


def main():

    methods = [
        # 'fiber_query',
        # 'fss_10k',
        'reco_bundle_10k',
        # 'ssn'
    ]

    gt_base_path = "/media/UG3/xieyu/fiber_query/HCP/HCP_mask/"

    pred_base_path = "/media/UG3/xieyu/fiber_query/HCP/fiber_recognize_results_mask/"

    out_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    bundle_names = get_bundle_names()

    subjects = os.listdir(gt_base_path)

    for subject in tqdm(subjects):
        cur_gt_base_dir = os.path.join(gt_base_path, subject)
        cur_out_dir = os.path.join(out_base_path, subject)
        for method in methods:
            cur_dice = {}
            cur_out_path = os.path.join(cur_out_dir, f"{method}_volumn_metrics.json")
            if os.path.exists(cur_out_path):
                continue

            if not os.path.exists(os.path.join(pred_base_path, subject, f"{method}_results")):
                continue
            for bundle_name in tqdm(bundle_names):
                cur_gt = os.path.join(cur_gt_base_dir, f"{bundle_name}.nii.gz")
                cur_pred = os.path.join(pred_base_path, subject, f"{method}_results/{bundle_name}.nii.gz")
                cur_dice[bundle_name] = get_metrics(cur_gt, cur_pred)

            write_dict_2_json(cur_dice, cur_out_path)


if __name__ == '__main__':
    main()
