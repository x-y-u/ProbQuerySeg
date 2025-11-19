#!/bin/bash

# 根目录，可以根据实际情况修改
ROOT_DIR="/media/UG5/BTC"
DWI_dir="/media/UG3/xieyu/fiber_query/BTC/tractseg_results"
t1w_base_dir="/media/UG3/xieyu/fiber_query/BTC/T1_un_reg/"

# 遍历 BTC_preop 和 BTC_postop 下所有 sub-CON* 和 sub-PAT*
for dir in "$ROOT_DIR"/BTC_*/sub-*/ses-*/proc/; do
    dir="/media/UG5/BTC/BTC_postop/sub-CON02/ses-postop/proc/"
    if [ -d "$dir" ]; then
        # 获取样本ID，比如 sub-CON04
        sample=$(basename "$(dirname "$(dirname "$dir")")")

        # 获取 session，比如 preop
        session_full=$(basename "$(dirname "$dir")")   # ses-preop
        session=${session_full#ses-}

        echo "处理样本: $sample, 会话: $session, 路径: $dir"

        output_path="/media/UG3/xieyu/fiber_query/BTC/metrics/${session}_${sample}"

        org_file_path="${DWI_dir}/${session}_${sample}/DWI.mif"
        t1w_path="${t1w_base_dir}/${session}_${sample}/t1w.nii.gz"
        mask_file_path="${dir}/dwi_mask.nii.gz"

        if [ ! -f "$org_file_path" ]; then
            echo "File not found: $org_file_path. Skipping ${session}_${sample}..."
            continue
        fi

        ./generate_fa.sh ${org_file_path} ${t1w_path} ${mask_file_path} ${output_path}
    fi
    break
done