#!/bin/bash

subject_base_dir="/data/xy/HCPD/T1_un_reg"

# 输出目录根路径
out_base="/data/xy/HCPD/T1_2_dwi_reg"

b0_base="/data/xy/HCPD/b0"

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
        -f "${b0_base}/${subject}/b0.nii.gz" \
        -m "${subject_base_dir}/${subject}/t1w.nii.gz" \
        -o "${out_dir}/${subject}_to_dwi_" &

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