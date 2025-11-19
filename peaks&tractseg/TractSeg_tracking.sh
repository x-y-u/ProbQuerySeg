#!/bin/bash


TractSeg_tracking(){

    local peaks_path=$1

    TractSeg -i ${peaks_path} --output_type tract_segmentation
    TractSeg -i ${peaks_path} --output_type endings_segmentation
    TractSeg -i ${peaks_path} --output_type TOM
    Tracking -i ${peaks_path} --nr_fibers 20000
}


TractSeg_tracking "$@"