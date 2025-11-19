#!/bin/bash

#subject_base_dir="/data/xy/HCP_mask"

subject_base_dir="/data/xy/HCP_end_points_mask"

# 输出目录根路径
out_base="/data/xy/HCP_end_points_mask_reg"

reg_dir="/data/xy/HCP_T1_reg"

# MNI 模板路径
mni_template="/data/xy/HCP_105_T1_un_reg/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii"

for sub_dir in "$subject_base_dir"/*/; do

    # 提取 subject ID
    subject=$(basename "$sub_dir")
    out_dir="${out_base}/${subject}"
    mkdir -p "$out_dir"

    echo "Launching registration for subject: $subject"

    for sub_bundle in "$subject_base_dir"/"$subject"/*; do
        echo "$sub_bundle"

        bundle=$(basename "$sub_bundle")
        out_path="${out_dir}/${bundle}"

#        antsApplyTransforms \
#            -d 3 \
#            -i "$sub_bundle" \
#            -r "$mni_template" \
#            -o "$out_path" \
#            -n NearestNeighbor \
#            -t "${reg_dir}/${subject}/${subject}_to_MNI_1Warp.nii.gz" \
#            -t "${reg_dir}/${subject}/${subject}_to_MNI_0GenericAffine.mat"

        WarpImageMultiTransform 3 \
            "$sub_bundle" \
            "$out_path" \
            "${reg_dir}/${subject}/${subject}_to_MNI_1Warp.nii.gz" \
            "${reg_dir}/${subject}/${subject}_to_MNI_0GenericAffine.mat" \
            -R "$mni_template" \
            --use-NN

    done
done

# 最后一批任务也要等待完成
#wait

echo "All registrations completed."

