#!/bin/bash

base_dir="/media/UG5/AOMIC/PIOP1/derivatives/dwipreproc/"

# 设置文件夹名字的前缀和后缀
prefix="sub-"

# 循环遍历文件夹
for i in {1..50}; do
    # 使用 printf 格式化数字为三位数，并构建文件夹名字
    sub_idx="${prefix}$(printf "%04d" $i)"
    org_file_path="${base_dir}/${sub_idx}/dwi/${sub_idx}_desc-preproc_dwi.nii.gz"
    bval_file_path="${base_dir}/${sub_idx}/dwi/${sub_idx}_desc-preproc_dwi.bval"
    bvec_file_path="${base_dir}/${sub_idx}/dwi/${sub_idx}_desc-preproc_dwi.bvec"
    output_path="/media/UG3/xieyu/fiber_query/AOMIC/${sub_idx}"
    mask_file_path="${base_dir}/${sub_idx}/dwi/${sub_idx}_desc-brain_mask.nii.gz"

    if [ ! -f "$org_file_path" ]; then
        echo "File not found: $org_file_path. Skipping ${sub_idx}..."
        continue
    fi

    ./generate_peaks.sh ${org_file_path} ${bval_file_path} ${bvec_file_path} ${mask_file_path} ${output_path}

done


