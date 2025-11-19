#!/bin/bash

subject_base_dir="/media/UG3/xieyu/tractography_generate/HCP/HCP_tracts_tck/"

# 输入 T1 图像目录
t1_dir="/media/UG5/HCP"

# 输出目录根路径
out_base="/media/UG3/xieyu/tractography_generate/HCP/T1_reg"

# MNI 模板路径
mni_template="/media/UG5/Atlas/MNI/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii"

# 设置最大并行进程数
max_jobs=20

# 当前进程数
job_count=0

for sub_dir in "$subject_base_dir"/*/; do

    # 提取 subject ID
    subject=$(basename "$sub_dir")
    out_dir="${out_base}/${subject}"
    mkdir -p "$out_dir"

    echo "Launching registration for subject: $subject"

    # 启动后台任务
    antsRegistrationSyN.sh \
        -d 3 \
        -f "$mni_template" \
        -m "${t1_dir}/${subject}/T1w/T1w_acpc_dc_restore_brain.nii.gz" \
        -o "${out_dir}/${subject}_to_MNI_" &

    # 后台进程数加1
    ((job_count++))

    # 如果已达到最大并行数，等待所有任务完成
    if [[ "$job_count" -ge "$max_jobs" ]]; then
        wait
        job_count=0
    fi
done

# 最后一批任务也要等待完成
wait

echo "All registrations completed."

