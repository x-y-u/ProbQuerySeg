#!/bin/bash

#!/bin/bash

# 根目录，可以根据实际情况修改
ROOT_DIR="/media/UG5/BTC"

# 遍历 BTC_preop 和 BTC_postop 下所有 sub-CON* 和 sub-PAT*
for dir in "$ROOT_DIR"/BTC_*/sub-*/ses-*/proc/; do
    if [ -d "$dir" ]; then
        # 获取样本ID，比如 sub-CON04
        sample=$(basename "$(dirname "$(dirname "$dir")")")

        # 获取 session，比如 preop
        session_full=$(basename "$(dirname "$dir")")   # ses-preop
        session=${session_full#ses-}

        echo "处理样本: $sample, 会话: $session, 路径: $dir"

        output_path="/media/UG3/xieyu/fiber_query/BTC/tractseg_results/${session}_${sample}"

        org_file_path="${dir}/dwi.nii.gz"
        bval_file_path="${dir}/dwi.bval"
        bvec_file_path="${dir}/dwi.bvec"
        mask_file_path="${dir}/dwi_mask.nii.gz"

        if [ ! -f "$org_file_path" ]; then
            echo "File not found: $org_file_path. Skipping ${session}_${sample}..."
            continue
        fi

        ./generate_peaks.sh ${org_file_path} ${bval_file_path} ${bvec_file_path} ${mask_file_path} ${output_path}
    fi
done




## 设置文件夹名字的前缀和后缀
#prefix="sub-"
#
## 循环遍历文件夹
#for i in {15..161}; do
#    # 使用 printf 格式化数字为三位数，并构建文件夹名字
#    sub_idx="${prefix}$(printf "%03d" $i)"
#    org_file_path="/media/UG5/Caffine/${sub_idx}/proc/dwi.nii.gz"
#    bval_file_path="/media/UG5/Caffine/${sub_idx}/proc/dwi.bval"
#    bvec_file_path="/media/UG5/Caffine/${sub_idx}/proc/dwi.bvec"
#    output_path="/media/UG3/xieyu/fiber_query/Caffine/${sub_idx}"
#    mask_file_path="/media/UG5/Caffine/${sub_idx}/proc/dwi_mask.nii.gz"
#
#    if [ ! -f "$org_file_path" ]; then
#        echo "File not found: $org_file_path. Skipping ${sub_idx}..."
#        continue
#    fi
#
#    ./generate_peaks.sh ${org_file_path} ${bval_file_path} ${bvec_file_path} ${mask_file_path} ${output_path}
#
#done


