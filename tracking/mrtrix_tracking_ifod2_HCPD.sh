#!/bin/bash

freesurfer_base_dir="/media/UG3/xieyu/fiber_query/HCPD/freesurfer_out"

fod_base_dir="/media/UG3/xieyu/fiber_query/HCPD/tractseg_output"

mask_base_dir="/media/UG5/HCPD"

out_base_dir="/media/UG3/xieyu/fiber_query/HCPD/tracking_results"

for sub_dir in "${freesurfer_base_dir}"/*/; do
    sub_idx=$(basename "$sub_dir")

    cur_5tt_path="${sub_dir}/5TT.mif"
    cur_wmgmi_path="${sub_dir}/wmgmi.nii.gz"

    cur_wm_fod_path="${fod_base_dir}/${sub_idx}/WM_FODs.mif"
    cur_out_dir="${out_base_dir}/${sub_idx}"
    cur_mask_path="${mask_base_dir}/${sub_idx}/T1w/Diffusion/nodif_brain_mask.nii.gz"

    mkdir -p ${cur_out_dir}

#    tckgen -algorithm iFOD2 -act ${cur_5tt_path} -crop_at_gmwmi -cutoff 0.01 -angle 60 -select 1M -seed_gmwmi ${cur_wmgmi_path} \
#    ${cur_wm_fod_path} ${cur_out_dir}/track_ifod2_rk4_wmgmi_1M_step_30.tck -mask ${cur_mask_path} -minlength 20 -maxlength 250

    # command 4
    tckgen -algorithm iFOD1 -act ${cur_5tt_path} -crop_at_gmwmi -cutoff 0.01 -select 1M -rk4 -seed_dynamic ${cur_wm_fod_path} ${cur_wm_fod_path} \
    ${cur_out_dir}/track_ifod1_rk4_dynamic_1M.tck -mask ${cur_mask_path} -minlength 20 -maxlength 250

#    # command 5
#    tckgen -algorithm iFOD1 -act ${cur_5tt_path} -crop_at_gmwmi -cutoff 0.01 -rk4 -seed_grid_per_voxel ${cur_mask_path} 2 ${cur_wm_fod_path} \
#    ${cur_out_dir}/track_ifod1_rk4_seed_1M.tck -mask ${cur_mask_path} -minlength 20 -maxlength 250
#
#    # command 6
#    tckgen -algorithm iFOD1 -act ${cur_5tt_path} -crop_at_gmwmi -cutoff 0.01 -angle 30 -select 1M -rk4 \
#    -seed_dynamic ${cur_wm_fod_path} ${cur_wm_fod_path} ${cur_out_dir}/track_ifod1_rk4_dynamic_1M_step_30.tck -mask ${cur_mask_path} -minlength 20 -maxlength 250
#
#    # command 7
#    tckgen -algorithm iFOD1 -act ${cur_5tt_path} -crop_at_gmwmi -cutoff 0.01 -angle 30 -rk4 \
#    -seed_grid_per_voxel ${cur_mask_path} 2 ${cur_wm_fod_path} ${cur_out_dir}/track_ifod1_rk4_seed_1M_step_30.tck -mask ${cur_mask_path} -minlength 20 -maxlength 250
#
#    # command 8
#    tckgen -algorithm iFOD1 -act ${cur_5tt_path} -crop_at_gmwmi -cutoff 0.01 -select 1M -rk4 \
#    -seed_gmwmi ${cur_wmgmi_path} ${cur_wm_fod_path} ${cur_out_dir}/track_ifod1_rk4_wmgmi_1M.tck -mask ${cur_mask_path} -minlength 20 -maxlength 250
#
#    # command 9
#    tckgen -algorithm iFOD1 -act ${cur_5tt_path} -crop_at_gmwmi -cutoff 0.01 -angle 30 -select 1M -rk4 \
#    -seed_gmwmi ${cur_wmgmi_path} ${cur_wm_fod_path} ${cur_out_dir}/track_ifod1_rk4_wmgmi_1M_step_30.tck -mask ${cur_mask_path} -minlength 20 -maxlength 250
done



#session="postop"
#id="sub-CON04"
#sub_id=${session}_${id}
#
#
#cur_5tt_path="/media/UG3/xieyu/fiber_query/BTC/freesurfer_out/${sub_id}/5TT.mif"
#cur_wmgmi_path="/media/UG3/xieyu/fiber_query/BTC/freesurfer_out/${sub_id}/wmgmi.nii.gz"
#
#cur_wm_fod_path="/media/UG3/xieyu/fiber_query/BTC/tractseg_results/${sub_id}/WM_FODs.mif"
#cur_out_dir="/media/UG3/xieyu/fiber_query/BTC/tracking_results/${sub_id}"
#cur_mask_path="/media/UG5/BTC/BTC_${session}/${id}/ses-postop/proc/dwi_mask.nii.gz"
#
#mkdir -p ${cur_out_dir}
#
#tckgen -algorithm iFOD2 -act ${cur_5tt_path} -crop_at_gmwmi -cutoff 0.01 -angle 60 -select 1M -seed_gmwmi ${cur_wmgmi_path} \
#${cur_wm_fod_path} ${cur_out_dir}/track_ifod2_rk4_wmgmi_1M_step_30.tck -mask ${cur_mask_path} -minlength 20 -maxlength 250
