#!/bin/bash

generate_MNI_atlas(){
  input_dir=$1
  warp_file=$2
  output_dir=$3

  mkdir -p "$output_dir"

  for tck_file in "${input_dir}"/*.tck; do
      fname=$(basename "$tck_file")   # 取文件名
      echo "Processing $fname"
      tcktransform "$tck_file" \
                   "$warp_file" \
                   "${output_dir}/${fname}" -force
  done
}

#generate_MNI_atlas \
#  "/media/UG3/xieyu/fiber_query/HCP/HCP_tracts_tck/620434/tracts" \
#  "/media/UG3/xieyu/fiber_query/HCP/T1_reg/620434/mrtrix_warp_corrected_for_track_Sub2Atlas.mif" \
#  "/media/UG3/xieyu/fiber_query/HCP/MNI_tck/620434/"

for sub_dir in /media/UG3/xieyu/fiber_query/HCP/HCP_tracts_tck/*; do
    sub_id=$(basename "$sub_dir")   # 获取样本 ID
    echo "Processing subject: $sub_id"

    input_dir="/media/UG3/xieyu/fiber_query/HCP/HCP_tracts_tck/${sub_id}/tracts"
    warp_file="/media/UG3/xieyu/fiber_query/HCP/T1_reg/${sub_id}/mrtrix_warp_corrected_for_track_Sub2Atlas.mif"
    output_dir="/media/UG3/xieyu/fiber_query/HCP/MNI_tck/${sub_id}"

    if [[ -d "$input_dir" && -f "$warp_file" ]]; then
        generate_MNI_atlas "$input_dir" "$warp_file" "$output_dir"
    else
        echo "Skipping $sub_id (missing input or warp file)"
    fi
done