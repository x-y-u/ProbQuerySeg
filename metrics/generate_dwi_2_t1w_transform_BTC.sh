#!/bin/bash

metrics_base_dir="/media/UG3/xieyu/fiber_query/BTC/metrics"

dwi_path="/media/UG3/xieyu/fiber_query/BTC/tractseg_results/postop_sub-CON02/DWI.mif"
t1w_path="/media/UG3/xieyu/fiber_query/BTC/T1_un_reg/postop_sub-CON02/t1w.nii.gz"
output_dir="/media/UG3/xieyu/fiber_query/BTC/dwi_2_t1w_transform/postop_sub-CON02"


#./generate_dwi_2_t1w_transform.sh ${dwi_path} ${t1w_path} ${output_dir}


#mrtransform ${metrics_base_dir}/postop_sub-CON02/fa.mif -linear ${output_dir}/dwi2T1_rigid.txt -template ${t1w_path} ${metrics_base_dir}/postop_sub-CON02/fa_registered.mif -force

mrtransform ${metrics_base_dir}/postop_sub-CON02/fa.mif -template ${t1w_path} ${metrics_base_dir}/postop_sub-CON02/fa_registered.mif -force

