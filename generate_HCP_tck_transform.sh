#!/bin/bash

# 固定路径
reg_T1_base_path="/data/xy/Caffine/T1_reg"
un_reg_T1_base_path="/data/xy/Caffine/T1_un_reg"
atlas_base_path="/data/xy/HCP_105_T1_un_reg"
atlas_path="${atlas_base_path}/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii"

# 循环处理 HCP_T1_reg 下的所有样本
for reg_dir in "${reg_T1_base_path}"/*; do
    if [ -d "$reg_dir" ]; then
        subject_id=$(basename "$reg_dir")
        un_reg_T1_path="${un_reg_T1_base_path}/${subject_id}/t1w.nii.gz"

        echo "Processing subject: $subject_id"

        ./generate_tck_transform.sh \
            "$reg_dir" \
            "$atlas_base_path" \
            "$atlas_path" \
            "$un_reg_T1_path" \
            "$subject_id"
    fi
done


