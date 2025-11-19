#!/bin/bash

# 设置文件夹名字的前缀和后缀
prefix="sub-"

# 循环遍历文件夹
for i in {15..161}; do
    # 使用 printf 格式化数字为三位数，并构建文件夹名字
    sub_idx="${prefix}$(printf "%03d" $i)"
    org_file_path="/media/UG5/Caffine/${sub_idx}/proc/dwi.nii.gz"
    bval_file_path="/media/UG5/Caffine/${sub_idx}/proc/dwi.bval"
    bvec_file_path="/media/UG5/Caffine/${sub_idx}/proc/dwi.bvec"
    output_path="/media/UG3/xieyu/fiber_query/Caffine/${sub_idx}"
    mask_file_path="/media/UG5/Caffine/${sub_idx}/proc/dwi_mask.nii.gz"

    if [ ! -f "$org_file_path" ]; then
        echo "File not found: $org_file_path. Skipping ${sub_idx}..."
        continue
    fi

    ./generate_peaks.sh ${org_file_path} ${bval_file_path} ${bvec_file_path} ${mask_file_path} ${output_path}

done


