#!/bin/bash

subject_base_dir="/data/xy/HCP_mask"

# 输出目录根路径
out_base="/data/xy/multi_mask_label_to_person"

mkdir -p "$out_base"

label_path="/data/xy/MNI_label/multi_mask_label.nii.gz"

person_t1_base_path="/data/xy/HCP_105_T1_un_reg"

reg_dir="/data/xy/HCP_T1_reg"

for sub_dir in "$subject_base_dir"/*/; do

    # 提取 subject ID
    subject=$(basename "$sub_dir")
    out_path="${out_base}/${subject}.nii.gz"

    echo "Launching registration for subject: $subject"

    WarpImageMultiTransform 3 \
        "$label_path" \
        "$out_path" \
        -R "$person_t1_base_path/$subject/T1w_acpc_dc_restore_brain.nii.gz" \
        -i "${reg_dir}/${subject}/${subject}_to_MNI_0GenericAffine.mat" \
        "${reg_dir}/${subject}/${subject}_to_MNI_1InverseWarp.nii.gz" \
        --use-NN
done

# 最后一批任务也要等待完成
#wait

echo "All registrations completed."