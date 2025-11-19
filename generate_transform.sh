#!/bin/bash


warpinit /media/UG3/xieyu/tractography_generate/HCP/HCP_tracts_tck/620434/DWI.mif /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/identity_warp[].nii.gz



mrconvert subj_dwi.nii.gz subj_dwi.mif

# 生成三张 identity 图（X/Y/Z 坐标）
warpinit /media/UG3/xieyu/tractography_generate/HCP/HCP_tracts_tck/620434/DWI.mif /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/id.mif
mrconvert /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/id.mif /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/id_X.nii.gz -coord 3 0
mrconvert /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/id.mif /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/id_Y.nii.gz -coord 3 1
mrconvert /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/id.mif /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/id_Z.nii.gz -coord 3 2

antsApplyTransforms -d 3 -i /data/xy/MNI_tck/620434/id_Z.nii.gz -r /data/xy/HCP_105_T1_un_reg/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii \
  -t /data/xy/HCP_T1_reg/620434/620434_to_MNI_1Warp.nii.gz \
  -t /data/xy/HCP_T1_reg/620434/620434_to_MNI_0GenericAffine.mat \
  -o /data/xy/MNI_tck/620434/warped_Z.nii.gz -n Linear

antsApplyTransforms -d 3 -i id_Y.nii.gz -r TEMPLATE.nii.gz \
  -t SUBJ_to_TEMPLATE_1Warp.nii.gz \
  -t SUBJ_to_TEMPLATE_0GenericAffine.mat \
  -o warped_Y.nii.gz -n Linear

antsApplyTransforms -d 3 -i id_Z.nii.gz -r TEMPLATE.nii.gz \
  -t SUBJ_to_TEMPLATE_1Warp.nii.gz \
  -t SUBJ_to_TEMPLATE_0GenericAffine.mat \
  -o warped_Z.nii.gz -n Linear


mrcat /data/xy/MNI_tck/620434/mrtrix_warp0.nii.gz /data/xy/MNI_tck/620434/mrtrix_warp1.nii.gz /data/xy/MNI_tck/620434/mrtrix_warp2.nii.gz -axis 3 /data/xy/MNI_tck/620434/mrtrix_warp_uncorrected.mif

warpcorrect /data/xy/MNI_tck/620434/mrtrix_warp_uncorrected.mif /data/xy/MNI_tck/620434/mrtrix_warp_corrected.mif -marker 2147483647

warpcorrect /data/xy/MNI_tck/620434/mrtrix_warp[].nii /data/xy/MNI_tck/620434/inv_mrtrix_warp_corrected.mif -marker 2147483647

for i in {0..2}; do
  antsApplyTransforms -d 3 \
    -i /data/xy/MNI_tck/620434/identity_warp${i}.nii.gz \
    -o /data/xy/MNI_tck/620434/mrtrix_warp${i}.nii.gz \
    -r /data/xy/HCP_105_T1_un_reg/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii \
    -t /data/xy/HCP_T1_reg/620434/620434_to_MNI_1Warp.nii.gz \
    -t /data/xy/HCP_T1_reg/620434/620434_to_MNI_0GenericAffine.mat \
    --default-value 2147483647
done


WarpImageMultiTransform 3 \
  /data/xy/MNI_tck/620434/id_X.nii.gz \
  /data/xy/MNI_tck/620434/warped_X.nii.gz \
  /data/xy/HCP_T1_reg/620434/620434_to_MNI_1Warp.nii.gz \
  /data/xy/HCP_T1_reg/620434/620434_to_MNI_0GenericAffine.mat \
  -R /data/xy/HCP_105_T1_un_reg/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii -force


mrcat /data/xy/MNI_tck/620434/warped_X.nii.gz /data/xy/MNI_tck/620434/warped_Y.nii.gz /data/xy/MNI_tck/620434/warped_Z.nii.gz /data/xy/MNI_tck/620434/warped.mif -axis 3




T1=${subPath}/t1w_std_align_center_unring_unbiased_brain_in_dwi.nii.gz
Atlas=/home/wuye/D_disk/Atlas/MNI/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii

rm -r ${subPath}/MNI
mkdir -p ${subPath}/MNI
ANTS 3 -m PR[${Atlas},${T1},1,2] -o ${subPath}/MNI/Sub2Atlas.nii -i 30x99x11 -t SyN[0.5] -r Gauss[2,0] --use-Histogram-Matching --continue-affine true  > /dev/null 2>&1
ANTS 3 -m PR[${T1},${Atlas},1,2] -o ${subPath}/MNI/Atlas2Sub.nii -i 30x99x11 -t SyN[0.5] -r Gauss[2,0] --use-Histogram-Matching --continue-affine true  > /dev/null 2>&1


warpinit ${Atlas} ${subPath}/MNI/identity_warp[].nii -quiet > /dev/null 2>&1
for j in `seq 0 2`
do
WarpImageMultiTransform 3 ${subPath}/MNI/identity_warp${j}.nii ${subPath}/MNI/mrtrix_warp${j}.nii -R ${T1} ${subPath}/MNI/Atlas2SubWarp.nii ${subPath}/MNI/Atlas2SubAffine.txt > /dev/null 2>&1
done
warpcorrect ${subPath}/MNI/mrtrix_warp[].nii ${subPath}/MNI/mrtrix_warp_corrected_for_track_Sub2Atlas.mif -quiet > /dev/null 2>&1
rm ${subPath}/MNI/identity_warp*
rm ${subPath}/MNI/mrtrix_warp*.nii


warpinit ${T1} ${subPath}/MNI/identity_warp[].nii -quiet > /dev/null 2>&1
for j in `seq 0 2`
do
WarpImageMultiTransform 3 ${subPath}/MNI/identity_warp${j}.nii ${subPath}/MNI/mrtrix_warp${j}.nii -R ${Atlas} ${subPath}/MNI/Sub2AtlasWarp.nii ${subPath}/MNI/Sub2AtlasAffine.txt > /dev/null 2>&1
done
warpcorrect ${subPath}/MNI/mrtrix_warp[].nii ${subPath}/MNI/mrtrix_warp_corrected_for_track_Atlas2Sub.mif -quiet > /dev/null 2>&1
rm ${subPath}/MNI/identity_warp*
rm ${subPath}/MNI/mrtrix_warp*.nii


warpinit /data/xy/HCP_105_T1_un_reg/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii /data/xy/HCP_105_T1_un_reg/identity_warp[].nii -quiet > /dev/null 2>&1

for j in `seq 0 2`
do
WarpImageMultiTransform 3 /data/xy/HCP_105_T1_un_reg/MNI/identity_warp${j}.nii /data/xy/HCP_T1_reg/620434/mrtrix_warp${j}.nii -R /data/xy/HCP_105_T1_un_reg/620434/T1w_acpc_dc_restore_brain.nii.gz /data/xy/HCP_T1_reg/620434/Atlas2SubWarp.nii /data/xy/HCP_T1_reg/620434/Atlas2SubAffine.txt > /dev/null 2>&1
done
warpcorrect ${subPath}/MNI/mrtrix_warp[].nii ${subPath}/MNI/mrtrix_warp_corrected_for_track_Sub2Atlas.mif -quiet > /dev/null 2>&1
rm ${subPath}/MNI/identity_warp*
rm ${subPath}/MNI/mrtrix_warp*.nii


