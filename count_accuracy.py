"""
    coding: utf-8
    Project: Fiber_Query
    File: count_accuracy.py
    Author: xieyu
    Date: 2025/9/13 17:25
    IDE: PyCharm
"""
import os
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from utils import get_bundle_names


from collections import Counter

def misclassification_details(labels_path, pred_labels_path, bundle_names):
    y_true = np.load(labels_path).astype(int)              # shape: (N,)
    y_pred = np.load(pred_labels_path).astype(int)         # shape: (N, C)

    # 将预测 one-hot 转为类别索引
    # y_pred_cls = np.argmax(y_pred, axis=1)

    # 统计混淆矩阵
    num_classes = len(bundle_names)
    confusion = np.zeros((num_classes, num_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        if not np.all(p == 0):
            confusion[t, np.argmax(p)] += 1

    # 打印错分详情（只打印错分部分）
    for i in range(num_classes):
        for j in range(num_classes):
            if i != j and confusion[i, j] > 0:
                print(f"真实类别 {bundle_names[i]} 被错分为 {bundle_names[j]}: {confusion[i, j]} 次")

    return confusion


def count_single_sample(labels_path, pred_labels_path):
    bundle_names = get_bundle_names()
    misclassification_details(labels_path, pred_labels_path, bundle_names)
    y_true = np.load(labels_path).astype(int)
    y_pred = np.load(pred_labels_path).astype(int)

    # 转 one-hot
    y_true_onehot = np.zeros_like(y_pred)
    y_true_onehot[np.arange(len(y_true)), y_true] = 1

    # class_acc = (y_pred == y_true_onehot).sum(axis=0) / len(y_true)
    class_acc = ((y_pred == y_true_onehot) * (y_pred == 1)).sum(axis=0) / y_pred.sum(axis=0)
    class_acc2 = ((y_pred == y_true_onehot) * (y_true_onehot == 1)).sum(axis=0) / y_true_onehot.sum(axis=0)
    class_num = y_pred.sum(axis=0)
    class_num2 = y_true_onehot.sum(axis=0)
    for i, acc in enumerate(class_acc):
        print(bundle_names[i], class_num[i], class_num2[i], acc, class_acc2[i])
    # print("每个类别的准确率:", class_acc)
    #
    # # 精确率, 召回率, F1（逐类）
    # precision = precision_score(y_true_onehot, y_pred, average=None, zero_division=0)
    # recall = recall_score(y_true_onehot, y_pred, average=None, zero_division=0)
    # f1 = f1_score(y_true_onehot, y_pred, average=None, zero_division=0)
    #
    # print("逐类 Precision:", precision)
    # print("逐类 Recall:", recall)
    # print("逐类 F1:", f1)
    #
    # # 宏平均 (macro), 加权平均 (weighted), 微平均 (micro)
    # print("Macro F1:", f1_score(y_true_onehot, y_pred, average="macro"))
    # print("Micro F1:", f1_score(y_true_onehot, y_pred, average="micro"))

    sample_acc = ((y_pred[np.arange(len(y_true)), y_true] == 1)*(np.any(y_pred != 0, axis=1))).mean()
    print("样本级别准确率:", sample_acc)

    pass


def main():

    tck_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    sample_names = os.listdir(tck_base_path)

    sample_names = ['622236']

    for sample_name in sample_names:
        print(sample_name)
        cur_pred_labels_path = os.path.join(tck_base_path, sample_name, "fiber_query_labels.npy")
        cur_labels_path = os.path.join(tck_base_path, sample_name, "labels.npy")
        count_single_sample(cur_labels_path, cur_pred_labels_path)
        break

    # cur_pred_labels_path = os.path.join(tck_base_path, sample_names[0], "fiber_query_labels.npy")
    # cur_labels_path = os.path.join(tck_base_path, sample_names[0], "labels.npy")
    # count_single_sample(cur_labels_path, cur_pred_labels_path)

    # cur_pred_labels_path = os.path.join(tck_base_path, sample_names[0], "fss_labels.npy")
    # count_single_sample(cur_labels_path, cur_pred_labels_path)

    # for sample_name in sample_names:
    #     print(sample_name)
    #     cur_pred_labels_path = os.path.join(tck_base_path, sample_name, "fiber_query_labels.npy")
    #     cur_labels_path = os.path.join(tck_base_path, sample_name, "labels.npy")
    #
    #     count_single_sample(cur_labels_path, cur_pred_labels_path)


    pass


if __name__ == '__main__':
    main()
