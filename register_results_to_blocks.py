"""
    coding: utf-8
    Project: Fiber_Query
    File: register_results_to_blocks.py
    Author: xieyu
    Date: 2025/9/19 14:55
    IDE: PyCharm
"""
import os
import nibabel as nib
import numpy as np


def single_probability_mask_to_multi_mask(base_dir, out_dir):

    for bundle_mask in os.listdir(base_dir):
        print(bundle_mask)
        cur_mask_nii = nib.load(os.path.join(base_dir, bundle_mask))
        cur_mask = cur_mask_nii.get_fdata()

        cur_bundle_name = bundle_mask.split('.')[0]

        for i in np.arange(0, 1, 0.1):
            item_mask = (cur_mask > i).astype(np.uint8)
            # print(item_mask.shape)
            cur_out_path = os.path.join(out_dir, cur_bundle_name + '_' + f"{i:.1f}" + '.nii.gz')
            item_nii = nib.Nifti1Image(item_mask, affine=cur_mask_nii.affine, header=cur_mask_nii.header)
            nib.save(item_nii, cur_out_path)
        # break


def main():

    base_dir = "/media/UG3/xieyu/fiber_query/BTC/population_mask_in_person/postop_sub-CON02/"
    out_dir = "/media/UG3/xieyu/fiber_query/BTC/population_mask_in_person_uncorrected/postop_sub-CON02/"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    single_probability_mask_to_multi_mask(base_dir, out_dir)


    pass


if __name__ == '__main__':
    main()
