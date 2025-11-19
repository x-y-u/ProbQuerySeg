"""
    coding: utf-8
    Project: Fiber_Query
    File: recobundle_search.py
    Author: xieyu
    Date: 2025/9/17 11:04
    IDE: PyCharm
"""
import numpy as np
from dipy.io.stateful_tractogram import StatefulTractogram
from dipy.io.streamline import load_tractogram, save_tractogram

from dipy.segment.fss import FastStreamlineSearch
import os

from tqdm import tqdm

from utils import get_bundle_names

import os

import numpy as np
from tqdm import tqdm

from dipy.io.streamline import load_tractogram
from dipy.tracking.streamline import Streamlines
from dipy.segment.bundles import RecoBundles


def reco_bundle_search(atlas_bundle, target_bundle):
    # # radius = 7.0
    # rb = RecoBundles(atlas_bundle, verbose=True, rng=np.random.RandomState(2001))
    #
    # labels = []
    #
    # block_size = 10000
    # for j in tqdm(range(0, len(target_bundle), block_size)):
    #     # print(j)
    #     cur_target = target_bundle[j:j + block_size]
    #
    #     _, bundle_indices = rb.recognize(model_bundle=Streamlines(cur_target),
    #                                      model_clust_thr=0.1,
    #                                      reduction_thr=20,
    #                                      pruning_thr=7,
    #                                      reduction_distance='mdf',
    #                                      pruning_distance='mdf',
    #                                      slr=True)
    #     # print(bundle_indices)
    #     if len(bundle_indices) > 0:
    #         labels.extend(bundle_indices + j)
    #
    # # coo_mdist_mtx = cur_fst.radius_search(target_bundle, radius=radius)

    # radius = 7.0
    rb = RecoBundles(target_bundle, verbose=True, rng=np.random.RandomState(2001))

    _, labels = rb.recognize(model_bundle=Streamlines(atlas_bundle),
                                         model_clust_thr=0.1,
                                         reduction_thr=15,
                                         pruning_thr=7,
                                         reduction_distance='mdf',
                                         pruning_distance='mdf',
                                         slr=True)

    return labels
    return np.unique(coo_mdist_mtx.row)


def main():

    atlas_base_path = "/media/UG3/xieyu/fiber_query/HCP/Atlas_tck_in_person/"
    bundle_names = get_bundle_names()

    references_base_path = "/media/UG3/xieyu/fiber_query/HCP/T1_un_reg/"

    whole_brain_base_path = "/media/UG3/xieyu/fiber_query/HCP/whole_brain_bundles_in_person/"

    subjects = os.listdir(atlas_base_path)

    # subjects = ["599469"]

    atlas_nums = ["10k"]

    for subject in subjects:

        cur_whole_brain_path = os.path.join(whole_brain_base_path, subject, "whole_brain.tck")

        cur_reference_path = os.path.join(references_base_path, subject, "T1w_acpc_dc_restore_brain.nii.gz")
        cur_whole_brain_sft = load_tractogram(cur_whole_brain_path, reference=cur_reference_path, bbox_valid_check=False)
        cur_whole_brain = cur_whole_brain_sft.streamlines
        print(len(cur_whole_brain))

        # cur_out_base_path = os.path.join(whole_brain_base_path, subject, "fss_results")
        # if not os.path.exists(cur_out_base_path):
        #     os.makedirs(cur_out_base_path)

        cur_atlas_base_path = os.path.join(atlas_base_path, subject)

        for atlas_num in atlas_nums:
            if os.path.exists(os.path.join(whole_brain_base_path, subject, f"reco_bundle_{atlas_num}_labels.npy")):
                continue
            results = np.zeros((len(cur_whole_brain), len(bundle_names)), dtype=int)
            for i, bundle in tqdm(enumerate(bundle_names)):
                cur_atlas = load_tractogram(os.path.join(cur_atlas_base_path, f"{bundle}_{atlas_num}.tck"),
                                            reference=cur_reference_path, bbox_valid_check=False).streamlines
                print(len(cur_atlas))
                cur_fss_result = reco_bundle_search(cur_atlas, cur_whole_brain)
                print(len(cur_fss_result))

                results[np.array(cur_fss_result), i] = 1

                # cur_lines = [cur_whole_brain[item] for item in cur_fss_result]
                # cur_sft = StatefulTractogram(cur_lines, reference=cur_reference_path, space=cur_whole_brain_sft.space)
                #
                # save_tractogram(cur_sft, os.path.join(cur_out_base_path, f"{bundle}.tck"), bbox_valid_check=False)

            np.save(os.path.join(whole_brain_base_path, subject, f"reco_bundle_{atlas_num}_labels.npy"), results)

            # break

        # break


    pass


if __name__ == '__main__':
    main()
