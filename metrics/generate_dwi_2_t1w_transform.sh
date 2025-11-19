#!/bin/bash

generate_transform(){
    local dwi_path=$1
    local t1w_path=$2
    local output_dir=$3

    mkdir -p ${output_dir}

    dwiextract ${dwi_path} -bzero - | mrmath - mean ${output_dir}/mean_b0.mif -axis 3 -force

    mrregister ${output_dir}/mean_b0.mif ${t1w_path} -type rigid -rigid ${output_dir}/dwi2T1_rigid.txt -force

}

generate_transform "$@"

