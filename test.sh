


tckmap /media/UG3/xieyu/tractography_generate/HCP/HCP_tracts_tck/599469/tracts/AF_left.tck -template /media/UG5/HCP/599469/T1w/Diffusion/data.nii.gz /media/UG3/xieyu/tractography_generate/HCP/HCP_mask/599469/AF_left.nii.gz


rsync -avz -P xieyu@192.10.84.154:/media/UG3/xieyu/tractography_generate/HCP/T1_un_reg/* /data/xy/HCP_105_T1_un_reg/



rsync -avz -P /data/xy/HCP_T1_reg/* xieyu@192.10.84.154:/media/UG3/xieyu/tractography_generate/HCP/T1_reg/

rsync -avz -P xieyu@192.10.84.154:/media/UG3/xieyu/tractography_generate/HCP/HCP_mask/* /data/xy/HCP_mask/


rsync -avz -P /data/xy/HCP_mask_reg/* xieyu@192.10.84.154:/media/UG3/xieyu/tractography_generate/HCP/HCP_mask_reg/


mri_convert /media/UG5/Atlas/MNI/freesurfer/mri/aparc.a2009s+aseg.mgz /media/UG3/xieyu/mni/aparc.a2009s+aseg.nii.gz

tsfconvert /data/hyf/swm/hierarchy_clustering/atlas_version/scaler_replaced_7Network_top1.tsf /data/xieyu/hyf_data/scaler_replaced_7Network_top1.txt

tsfinfo /data/hyf/swm/hierarchy_clustering/atlas_version/scaler_replaced_7Network_top1.tsf

export PYTHONPATH=/path/to/your/mrtrix3/lib:$PYTHONPATH


export ANTSPATH=/opt/ants-2.5.4/bin
export PATH=$ANTSPATH:$PATH

rsync -avz -P xieyu@192.10.84.154:/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_plus/* /data/xy/HCP_multi_mask_plus/


rsync -avz -P xieyu@192.10.84.154:/media/UG3/xieyu/tractography_generate/HCP/MNI_bundle_probability_mask /data/xy/

rsync -avz -P /data/xy/end_points_multi_mask_label_in_person xieyu@192.10.84.154:/media/UG3/xieyu/tractography_generate/HCP/

rsync -avz -P xieyu@192.10.84.154:/media/UG3/xieyu/tractography_generate/HCP/HCP_multi_mask_reg_plus/* /data/xy/MNI_label/

rsync -avz -P /data/xy/HCP_end_points_mask_reg xieyu@192.10.84.154:/media/UG3/xieyu/tractography_generate/HCP/

rsync -avz -P xieyu@192.10.84.154:/media/UG3/xieyu/fiber_query/HCPD/freesurfer_out /data/xy/HCPD/

rsync -avz -P /data/xy/HCPD/T1_reg xieyu@192.10.84.154:/media/UG3/xieyu/fiber_query/HCPD/

rsync -avz -P /data/xy/HCPA/freesurfer_out xieyu@192.10.84.154:/media/UG3/xieyu/fiber_query/HCPA/

rsync -avz -P xieyu@192.10.84.154:/media/UG3/xieyu/fiber_query/HCPD/b0 /data/xy/HCPD/

rsync -avz -P /data/xy/BTC/freesurfer_out xieyu@192.10.84.154:/media/UG3/xieyu/fiber_query/BTC/


TractSeg -i /media/UG3/xieyu/fiber_query/Caffine/sub-015/peaks.nii.gz --output_type tract_segmentation
TractSeg -i /media/UG3/xieyu/fiber_query/Caffine/sub-015/peaks.nii.gz --output_type endings_segmentation
TractSeg -i /media/UG3/xieyu/fiber_query/Caffine/sub-015/peaks.nii.gz --output_type TOM
Tracking -i /media/UG3/xieyu/fiber_query/Caffine/sub-015/peaks.nii.gz --nr_fibers 20000


./transform_tck_to_mni.sh /media/UG3/xieyu/fiber_query/HCP/HCP_tracts_tck/620434/tracts/AF_left.tck /media/UG3/xieyu/fiber_query/HCP/T1_reg/620434/620434_to_MNI_0GenericAffine.mat /media/UG3/xieyu/fiber_query/HCP/T1_reg/620434/620434_to_MNI_1Warp.nii.gz /media/UG3/xieyu/fiber_query/HCP/T1_un_reg/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/AF_left.tck


tcktransform /media/UG3/xieyu/fiber_query/HCP/HCP_tracts_tck/620434/tracts/AF_left.tck \
  /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/mrtrix_warp_corrected.mif \
  /media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/AF_left.tck -force

./generate_tck_transform.sh /data/xy/HCP_T1_reg/620434 /data/xy/HCP_105_T1_un_reg /data/xy/HCP_105_T1_un_reg/mni_icbm152_t1_tal_nlin_asym_09a_brain.nii /data/xy/HCP_105_T1_un_reg/620434/T1w_acpc_dc_restore_brain.nii.gz 620434

WarpImageMultiTransform 3 /data/xy/HCP_105_T1_un_reg/identity_warp0.nii /data/xy/HCP_T1_reg/620434/mrtrix_warp0.nii -R /data/xy/HCP_105_T1_un_reg/620434/T1w_acpc_dc_restore_brain.nii.gz /data/xy/HCP_T1_reg/620434/620434_to_MNI_1InverseWarp.nii.gz /data/xy/HCP_T1_reg/620434/620434_to_MNI_0GenericAffine.mat > /dev/null 2>&1



export FREESURFER_HOME=/opt/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh

export FREESURFER_HOME=/opt/freesurfer
export PATH=$FREESURFER_HOME/bin:$PATH
export PATH=$FREESURFER_HOME/mni/bin:$PATH
export PATH=$FREESURFER_HOME/tktools:$PATH

export FREESURFER_HOME=/opt/freesurfer

export SUBJECTS_DIR=/data/xy/Caffine/freesurfer_out
recon-all -s sub-015 -i /data/xy/Caffine/T1_un_reg/sub-015/t1w.nii.gz -all

5ttgen freesurfer /data/xy/Caffine/freesurfer_out/sub-015/mri/aparc+aseg.mgz /data/xy/Caffine/freesurfer_out/sub-015/5TT.mif -lut /opt/freesurfer/FreeSurferColorLUT.txt -nocrop -sgm_amyg_hipp

5tt2gmwmi /data/xy/Caffine/freesurfer_out/sub-015/5TT.mif /data/xy/Caffine/freesurfer_out/sub-015/wmgmi.nii.gz

command11=['tckgen', '-algorithm', 'iFOD2', '-act', path_5TT_mif, '-crop_at_gmwmi', '-cutoff', '0.01', '-angle', '60', '-select', '1M',
                    '-seed_gmwmi', wmgmi_nii, dhollander_fod_wm_nii, track_ifod2_rk4_wmgmi_1M_step_30_tck,
                    '-mask', mask, '-minlength', '20', '-maxlength', '250']

tckgen -algorithm iFOD2 -act /media/UG3/xieyu/fiber_query/Caffine/freesurfer_out/sub-015/5TT.mif -crop_at_gmwmi -cutoff 0.01 -angle 60 \
-select 1M -seed_gmwmi /media/UG3/xieyu/fiber_query/Caffine/freesurfer_out/sub-015/wmgmi.nii.gz \
/media/UG3/xieyu/fiber_query/Caffine/sub-015/WM_FODs.mif /media/UG3/xieyu/fiber_query/Caffine/sub-015/track_ifod2_rk4_wmgmi_1M_step_30.tck \
-mask /media/UG5/Caffine/sub-015/proc/dwi_mask.nii.gz -minlength 20 -maxlength 250

mri_convert /data/xy/HCPA/freesurfer_out/*/mri/aparc.a2009s+aseg.mgz /data/xy/HCPA/freesurfer_out/*/mri/aparc.a2009s+aseg.nii.gz


mv /media/UG3/xieyu/fiber_query/HCPA/tracking_results/8867610/fiber_query_labels.npy /media/UG3/xieyu/fiber_query/HCPA/fiber_recognize_results/8867610/

export PATH=/opt/matlab/bin/:$PATH

matlab -nodisplay -nosplash -nodesktop -r "run('/home/xieyu/projects/Fiber_Query/matlab_code/demo.m'); exit;"


export FSLDIR=/opt/fsl
export PATH=${FSLDIR}/bin:${PATH}

