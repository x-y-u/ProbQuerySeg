#!/bin/bash

generate_fa(){
    local org_file_path=$1
    local t1w_path=$2
    local mask_file_path=$3
    local output_dir=$4

    mkdir -p ${output_dir}

    dwi2tensor ${org_file_path} ${output_dir}/tensor.mif -mask ${mask_file_path} -force
    tensor2metric ${output_dir}/tensor.mif -fa ${output_dir}/fa.mif -force

    mrtransform ${output_dir}/fa.mif -template ${t1w_path} ${output_dir}/fa_registered.mif -force

    mrconvert ${output_dir}/fa_registered.mif ${output_dir}/fa_registered.nii.gz -strides 1,2,3 -force

}

generate_fa "$@"
