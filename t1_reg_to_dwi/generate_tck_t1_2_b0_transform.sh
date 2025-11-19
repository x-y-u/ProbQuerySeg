#!/bin/bash

# 固定路径
reg_T1_base_path="/data/xy/HCPD/T1_2_dwi_reg"
un_reg_T1_base_path="/data/xy/HCPD/T1_un_reg"
target_base_path="/data/xy/HCPD/b0"

# 循环处理 HCP_T1_reg 下的所有样本
for reg_dir in "${reg_T1_base_path}"/*; do
    if [ -d "$reg_dir" ]; then
        subject_id=$(basename "$reg_dir")
        un_reg_T1_path="${un_reg_T1_base_path}/${subject_id}/T1w_acpc_dc_restore_brain.nii.gz"
        target_path="${target_base_path}/${subject_id}/b0.nii.gz"

        echo "Processing subject: $subject_id"

        ./generate_tck_transform.sh \
            "$reg_dir" \
            "$target_base_path/$subject_id" \
            "$target_path" \
            "$un_reg_T1_path" \
            "$subject_id"

        warpinit ${target_path} ${target_base_path}/${subject_id}/identity_warp[].nii -quiet > /dev/null 2>&1
        for j in `seq 0 2`
        do
        WarpImageMultiTransform 3 ${target_base_path}/${subject_id}/identity_warp${j}.nii ${reg_dir}/mrtrix_warp${j}.nii -R ${un_reg_T1_path} -i ${reg_dir}/${subject_id}_to_dwi_0GenericAffine.mat ${reg_dir}/${subject_id}_to_dwi_1InverseWarp.nii.gz > /dev/null 2>&1
        done
        warpcorrect ${reg_dir}/mrtrix_warp[].nii ${reg_dir}/mrtrix_warp_corrected_for_track_T1_2_DWI.mif -quiet > /dev/null 2>&1
        rm ${reg_dir}/mrtrix_warp*.nii
        rm ${target_base_path}/${subject_id}/identity_warp*.nii

        warpinit ${un_reg_T1_path} ${reg_dir}/identity_warp[].nii -quiet > /dev/null 2>&1
        for j in `seq 0 2`
        do
        WarpImageMultiTransform 3 ${reg_dir}/identity_warp${j}.nii ${reg_dir}/mrtrix_warp${j}.nii -R ${target_path} ${reg_dir}/${subject_id}_to_dwi_1Warp.nii.gz ${reg_dir}/${subject_id}_to_dwi_0GenericAffine.mat > /dev/null 2>&1
        done
        warpcorrect ${reg_dir}/mrtrix_warp[].nii ${reg_dir}/mrtrix_warp_corrected_for_track_DWI_2_T1.mif -quiet > /dev/null 2>&1
        rm ${reg_dir}/identity_warp*
        rm ${reg_dir}/mrtrix_warp*.nii
    fi
done


