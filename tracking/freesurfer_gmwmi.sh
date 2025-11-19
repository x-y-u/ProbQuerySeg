#!/bin/bash

T1_un_reg_base_dir="/data/xy/BTC/T1_un_reg"

out_base_dir="/data/xy/BTC/freesurfer_out"

export SUBJECTS_DIR=/data/xy/BTC/freesurfer_out
count=0

#id_list="preop_sub-PAT03 preop_sub-PAT06 preop_sub-PAT26"

for sub_dir in "${T1_un_reg_base_dir}"/*/; do
    sub_id=$(basename "$sub_dir")
#for sub_id in $id_list; do
    out_dir="${out_base_dir}/${sub_id}"

    if [ -f "${out_base_dir}/${sub_id}/wmgmi.nii.gz" ]; then
            echo "File already exists: ${sub_id}"
            continue
    fi

    recon-all -s ${sub_id} -i ${T1_un_reg_base_dir}/${sub_id}/t1w.nii.gz -all

    5ttgen freesurfer ${out_base_dir}/${sub_id}/mri/aparc+aseg.mgz ${out_base_dir}/${sub_id}/5TT.mif -lut /opt/freesurfer/FreeSurferColorLUT.txt -nocrop -sgm_amyg_hipp

    5tt2gmwmi ${out_base_dir}/${sub_id}/5TT.mif ${out_base_dir}/${sub_id}/wmgmi.nii.gz

    count=$((count+1))
    if [ "$count" -ge 5 ]; then
        break
    fi
done


