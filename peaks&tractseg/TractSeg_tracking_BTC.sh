#!/bin/bash

ROOT_DIR="/media/UG3/xieyu/fiber_query/BTC/tractseg_results"

id_list="preop_sub-PAT27 preop_sub-PAT28 preop_sub-PAT29 preop_sub-PAT31"

# 遍历 BTC_preop 和 BTC_postop 下所有 sub-CON* 和 sub-PAT*
for subject_id in $id_list; do
#    subject_id=$(basename "$dir")
    peaks_path="${ROOT_DIR}/${subject_id}/peaks.nii.gz"

    if [ ! -f "$peaks_path" ]; then
        echo "File not found: $peaks_path. Skipping ${subject_id}..."
        continue
    fi

    ./TractSeg_tracking.sh ${peaks_path}

done
