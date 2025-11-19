#!/bin/bash

#un_reg_T1=${subPath}/t1w_std_align_center_unring_unbiased_brain_in_dwi.nii.gz
#Atlas=/home/wuye/D_disk/Atlas/MNI/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii

#rm -r ${subPath}/MNI
#mkdir -p ${subPath}/MNI
#ANTS 3 -m PR[${Atlas},${T1},1,2] -o ${subPath}/MNI/Sub2Atlas.nii -i 30x99x11 -t SyN[0.5] -r Gauss[2,0] --use-Histogram-Matching --continue-affine true  > /dev/null 2>&1
#ANTS 3 -m PR[${T1},${Atlas},1,2] -o ${subPath}/MNI/Atlas2Sub.nii -i 30x99x11 -t SyN[0.5] -r Gauss[2,0] --use-Histogram-Matching --continue-affine true  > /dev/null 2>&1
#
#
#warpinit ${atlas_path} ${atlas_base_path}/identity_warp[].nii -quiet > /dev/null 2>&1

generate_tck_transform(){

  reg_base_path=$1
  atlas_base_path=$2
  atlas_path=$3
  un_reg_T1_path=$4
  subject_id=$5

  for j in `seq 0 2`
  do
  WarpImageMultiTransform 3 ${atlas_base_path}/identity_warp${j}.nii ${reg_base_path}/mrtrix_warp${j}.nii -R ${un_reg_T1_path} -i ${reg_base_path}/${subject_id}_to_MNI_0GenericAffine.mat ${reg_base_path}/${subject_id}_to_MNI_1InverseWarp.nii.gz > /dev/null 2>&1
  done
  warpcorrect ${reg_base_path}/mrtrix_warp[].nii ${reg_base_path}/mrtrix_warp_corrected_for_track_Sub2Atlas.mif -quiet > /dev/null 2>&1
  rm ${reg_base_path}/mrtrix_warp*.nii

  warpinit ${un_reg_T1_path} ${reg_base_path}/identity_warp[].nii -quiet > /dev/null 2>&1
  for j in `seq 0 2`
  do
  WarpImageMultiTransform 3 ${reg_base_path}/identity_warp${j}.nii ${reg_base_path}/mrtrix_warp${j}.nii -R ${atlas_path} ${reg_base_path}/${subject_id}_to_MNI_1Warp.nii.gz ${reg_base_path}/${subject_id}_to_MNI_0GenericAffine.mat > /dev/null 2>&1
  done
  warpcorrect ${reg_base_path}/mrtrix_warp[].nii ${reg_base_path}/mrtrix_warp_corrected_for_track_Atlas2Sub.mif -quiet > /dev/null 2>&1
  rm ${reg_base_path}/identity_warp*
  rm ${reg_base_path}/mrtrix_warp*.nii
}

generate_tck_transform "$@"


