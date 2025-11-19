#!/bin/bash

ROOT_DIR="/media/UG3/xieyu/fiber_query/HCPD/tractseg_output"

# 遍历 BTC_preop 和 BTC_postop 下所有 sub-CON* 和 sub-PAT*
for dir in "$ROOT_DIR"/*/; do
    subject_id=$(basename "$dir")
    peaks_path="${ROOT_DIR}/${subject_id}/peaks.nii.gz"

    if [ ! -f "$peaks_path" ]; then
        echo "File not found: $peaks_path. Skipping ${subject_id}..."
        continue
    fi

    ./TractSeg_tracking.sh ${peaks_path}

done
