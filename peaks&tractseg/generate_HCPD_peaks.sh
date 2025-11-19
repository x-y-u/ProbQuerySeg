#!/bin/bash

base_dir="/media/UG5/HCPD"
out_base_dir="/media/UG3/xieyu/fiber_query/HCPD/tractseg_output/"

mkdir -p ${out_base_dir}

# 循环遍历文件夹
for sub_dir in "${base_dir}"/*/; do
    # 使用 printf 格式化数字为三位数，并构建文件夹名字
    sub_idx=$(basename "$sub_dir")
    org_file_path="${base_dir}/${sub_idx}/T1w/Diffusion/data.nii.gz"
    bval_file_path="${base_dir}/${sub_idx}/T1w/Diffusion/bvals"
    bvec_file_path="${base_dir}/${sub_idx}/T1w/Diffusion/bvecs"
    output_path="${out_base_dir}/${sub_idx}"
    mask_file_path="${base_dir}/${sub_idx}/T1w/Diffusion/nodif_brain_mask.nii.gz"

    if [ ! -f "$org_file_path" ]; then
        echo "File not found: $org_file_path. Skipping ${sub_idx}..."
        continue
    fi

    ./generate_peaks.sh ${org_file_path} ${bval_file_path} ${bvec_file_path} ${mask_file_path} ${output_path}

done


