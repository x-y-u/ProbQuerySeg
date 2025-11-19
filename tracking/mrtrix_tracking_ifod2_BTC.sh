#!/bin/bash

freesurfer_base_dir="/media/UG3/xieyu/fiber_query/BTC/freesurfer_out"

fod_base_dir="/media/UG3/xieyu/fiber_query/BTC/tractseg_output"

mask_base_dir="/media/UG5/BTC"

out_base_dir="/media/UG3/xieyu/fiber_query/BTC/tracking_results"

for sub_dir in "${freesurfer_base_dir}"/*/; do
    sub_idx=$(basename "$sub_dir")
    session=${sub_idx%%_*}
    sample_id=${sub_idx#*_}

    cur_5tt_path="${sub_dir}/5TT.mif"
    cur_wmgmi_path="${sub_dir}/wmgmi.nii.gz"

    cur_wm_fod_path="${fod_base_dir}/${sub_idx}/WM_FODs.mif"
    cur_out_dir="${out_base_dir}/${sub_idx}"
    cur_mask_path="${mask_base_dir}/BTC_${session}/${sample_id}/ses-${session}/proc/dwi_mask.nii.gz"

    mkdir -p ${cur_out_dir}

    # command 4
    tckgen -algorithm iFOD1 -act ${cur_5tt_path} -crop_at_gmwmi -cutoff 0.01 -select 1M -rk4 -seed_dynamic ${cur_wm_fod_path} ${cur_wm_fod_path} \
    ${cur_out_dir}/track_ifod1_rk4_dynamic_1M.tck -mask ${cur_mask_path} -minlength 20 -maxlength 250

done
