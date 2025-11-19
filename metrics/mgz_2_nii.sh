#!/bin/bash

for subj in /data/xy/HCPA/freesurfer_out/*; do
    in_file="${subj}/mri/aparc.a2009s+aseg.mgz"
    out_file="${subj}/mri/aparc.a2009s+aseg.nii.gz"

    if [ -f "$in_file" ]; then
        mri_convert "$in_file" "$out_file"
    fi
done


