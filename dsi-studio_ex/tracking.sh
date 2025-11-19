#!/bin/bash

sub_base_dir="/media/UG3/xieyu/fiber_query/HCPA/T1_un_reg/"
base_dir="/media/UG5/HCPA"
dsi_studio="/media/UG3/dsi-studio/dsi_studio"

out_base_folder="/media/UG3/xieyu/fiber_query/HCPA/dsi_out"

# 遍历主文件夹下的所有子文件夹
for sub_dir in "$sub_base_dir"/*/; do
    sub_idx=$(basename "$sub_dir")
    # 检查是否是目录
    org_file_path="${base_dir}/${sub_idx}/T1w/Diffusion/data.nii.gz"
    bval_file_path="${base_dir}/${sub_idx}/T1w/Diffusion/bvals"
    bvec_file_path="${base_dir}/${sub_idx}/T1w/Diffusion/bvecs"
    mask_file_path="${base_dir}/${sub_idx}/T1w/Diffusion/nodif_brain_mask.nii.gz"

    cur_out_dir="${out_base_folder}/${sub_idx}"
    mkdir -p ${cur_out_dir}

    src_output_path="${cur_out_dir}/cur_src.src.gz"
    tck_output_path="${cur_out_dir}/cur_whole_brain.tck"
    rec_output_path="${cur_out_dir}/cur_fib.fib.gz"

    ${dsi_studio} --action=src --source=${org_file_path} --bval=${bval_file_path} --bvec=${bvec_file_path} --output=${src_output_path}
    sleep 5s

    ${dsi_studio} --action=rec --source=${src_output_path} --method=7 --param0=1.25 --other_output=all --record_odf=1 --check_btable=1 --mask=${mask_file_path} --output=${rec_output_path}
    sleep 5s

    ${dsi_studio} --action=trk --source=${rec_output_path} --output=${tck_output_path} --seed_count=1000000 --method=rk4 --thread_count=8
    sleep 5s
done


    
