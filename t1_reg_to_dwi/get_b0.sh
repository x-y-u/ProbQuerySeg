#!/bin/bash

base_dir="/media/UG3/xieyu/fiber_query/HCPD/tractseg_output"
out_dir="/media/UG3/xieyu/fiber_query/HCPD/b0"

mask_base="/media/UG5/HCPD"

for sub_dir in "${base_dir}"/*/; do
    sub_idx=$(basename "$sub_dir")

    mask_path="${mask_base}/${sub_idx}/T1w/Diffusion/nodif_brain_mask.nii.gz"

    mkdir -p ${out_dir}/${sub_idx}

#    dwiextract ${sub_dir}/DWI.mif - -bzero | mrmath - mean ${out_dir}/${sub_idx}/b0.nii.gz -axis 3

    dwiextract ${sub_dir}/DWI.mif - -bzero | mrmath - mean -axis 3 - | mrcalc - ${mask_path} -mult ${out_dir}/${sub_idx}/b0.nii.gz

done

