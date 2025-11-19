#!/bin/bash

base_dir="/data/xy/HCPD/freesurfer_out/"

for sub_dir in "${base_dir}"/*/; do
    sub_id=$(basename "$sub_dir")

    mri_convert ${base_dir}/${sub_id}/mri/aparc+aseg.nii.gz ${base_dir}/${sub_id}/mri/aparc+aseg.mgz

    5ttgen freesurfer ${base_dir}/${sub_id}/mri/aparc+aseg.mgz ${base_dir}/${sub_id}/5TT.mif -lut /opt/freesurfer/FreeSurferColorLUT.txt -nocrop -sgm_amyg_hipp

    5tt2gmwmi ${base_dir}/${sub_id}/5TT.mif ${base_dir}/${sub_id}/wmgmi.nii.gz

done
