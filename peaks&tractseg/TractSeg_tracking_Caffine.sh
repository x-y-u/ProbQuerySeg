#!/bin/bash

# 设置文件夹名字的前缀和后缀
prefix="sub-"

# 循环遍历文件夹
for i in {15..161}; do
    # 使用 printf 格式化数字为三位数，并构建文件夹名字
    sub_idx="${prefix}$(printf "%03d" $i)"
    peaks_path="/media/UG3/xieyu/fiber_query/Caffine/${sub_idx}/peaks.nii.gz"

    if [ ! -f "$peaks_path" ]; then
        echo "File not found: $peaks_path. Skipping ${sub_idx}..."
        continue
    fi

    ./TractSeg_tracking.sh ${peaks_path}

done
