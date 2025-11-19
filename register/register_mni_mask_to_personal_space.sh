#!/bin/bash

subject_base_dir="/data/xy/Caffine/T1_un_reg/"

# 输出目录根路径
out_base="/data/xy/Caffine/population_mask_in_person"

mni_base_dir="/data/xy/MNI_bundle_probability_mask"

person_t1_base_path="/data/xy/Caffine/T1_un_reg"

reg_dir="/data/xy/Caffine/T1_reg"

for sub_dir in "$subject_base_dir"/*/; do

    # 提取 subject ID
    subject=$(basename "$sub_dir")
    out_dir="${out_base}/${subject}"
    mkdir -p "$out_dir"

    echo "Launching registration for subject: $subject"

    for sub_bundle in "$mni_base_dir"/*; do
        echo "$sub_bundle"

        bundle=$(basename "$sub_bundle")
        out_path="${out_dir}/${bundle}"

#        antsApplyTransforms \
#            -d 3 \
#            -i "$mni_base_dir/$bundle" \
#            -r "$person_t1_base_path/$subject/T1w_acpc_dc_restore_brain.nii.gz" \
#            -o "$out_path" \
#            -n Linear \
#            -t "${reg_dir}/${subject}/${subject}_to_MNI_0GenericAffine.mat" \
#            -t "${reg_dir}/${subject}/${subject}_to_MNI_1InverseWarp.nii.gz"

        WarpImageMultiTransform 3 \
            "$mni_base_dir/$bundle" \
            "$out_path" \
            -R "$person_t1_base_path/$subject/t1w.nii.gz" \
            -i "${reg_dir}/${subject}/${subject}_to_MNI_0GenericAffine.mat" \
            "${reg_dir}/${subject}/${subject}_to_MNI_1InverseWarp.nii.gz"

    done
done

# 最后一批任务也要等待完成
#wait

echo "All registrations completed."