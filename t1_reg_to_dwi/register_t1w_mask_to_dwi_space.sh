#!/bin/bash

subject_base_dir="/data/xy/HCPD/T1_2_dwi_reg"

# 输出目录根路径
out_base="/data/xy/HCPD/population_mask_in_dwi"

mni_base_dir="/data/xy/HCPD/population_mask_in_person"

person_b0_base_path="/data/xy/HCPD/b0"

reg_dir="/data/xy/HCPD/T1_2_dwi_reg"

un_reg_t1_dir="/data/xy/HCPD/T1_un_reg"

for sub_dir in "$subject_base_dir"/*/; do

    # 提取 subject ID
    subject=$(basename "$sub_dir")
    out_dir="${out_base}/${subject}"
    mkdir -p "$out_dir"

    echo "Launching registration for subject: $subject"

    for sub_bundle in "$mni_base_dir"/"$subject"/*; do
        echo "$sub_bundle"

        bundle=$(basename "$sub_bundle")
        out_path="${out_dir}/${bundle}"

#        WarpImageMultiTransform 3 \
#            "$sub_bundle" \
#            "$out_path" \
#            -R "$person_b0_base_path/$subject/b0.nii.gz" \
#            -i "${reg_dir}/${subject}/${subject}_to_dwi_0GenericAffine.mat" \
#            "${reg_dir}/${subject}/${subject}_to_dwi_1InverseWarp.nii.gz"

        WarpImageMultiTransform 3 \
            "$sub_bundle" \
            "$out_path" \
            -R "$person_b0_base_path/$subject/b0.nii.gz" \
            "${reg_dir}/${subject}/${subject}_to_dwi_1InverseWarp.nii.gz" \
            "${reg_dir}/${subject}/${subject}_to_dwi_0GenericAffine.mat"

    done
    break
done

# 最后一批任务也要等待完成
#wait

echo "All registrations completed."