#!/bin/bash

generate_peaks(){
    local org_file_path=$1
    local bval_file_path=$2
    local bvec_file_path=$3
    local mask_file_path=$4
    local output_path=$5

    mkdir -p ${output_path}

    tmp_dwi="${output_path}/dwi.mif"

    mrconvert "${org_file_path}" -fslgrad "${bvec_file_path}" "${bval_file_path}" ${tmp_dwi}

    mrconvert "${tmp_dwi}" ${output_path}/DWI.mif -datatype float32 -strides 0,0,0,1
    dwi2response dhollander ${output_path}/DWI.mif ${output_path}/RF_WM.txt ${output_path}/RF_GM.txt ${output_path}/RF_CSF.txt
#    dwi2fod msmt_csd ${output_path}/DWI.mif ${output_path}/RF_WM.txt ${output_path}/WM_FODs.mif ${output_path}/RF_GM.txt ${output_path}/GM.mif ${output_path}/RF_CSF.txt ${output_path}/CSF.mif -mask ${mask_file_path}
#    sh2peaks ${output_path}/WM_FODs.mif ${output_path}/peaks.nii.gz -mask ${mask_file_path}
    dwi2fod msmt_csd ${output_path}/DWI.mif ${output_path}/RF_WM.txt ${output_path}/WM_FODs.mif ${output_path}/RF_GM.txt ${output_path}/GM.mif ${output_path}/RF_CSF.txt ${output_path}/CSF.mif -mask ${mask_file_path}
    sh2peaks ${output_path}/WM_FODs.mif ${output_path}/peaks.nii.gz -mask ${mask_file_path}

#    mrconvert ${output_path}/WM_FODs.mif ${output_path}/WM_FODs.nii.gz -force

}

generate_peaks "$@"
