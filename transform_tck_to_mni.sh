#!/bin/bash


transform_tck_to_mni(){
  local input_tck_path=$1
  local transform_path=$2
  local warp_path=$3
  local template_path=$4
  local output_path=$5

  tcktransform \
  ${input_tck_path} \
  -transform ${transform_path} \
  -warp ${warp_path} \
  -template ${template_path} \
  ${output_path} \
  -force

}


transform_tck_to_mni "$@"
