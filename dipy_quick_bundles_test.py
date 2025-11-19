"""
    coding: utf-8
    Project: Fiber_Query
    File: dipy_quick_bundles_test.py
    Author: xieyu
    Date: 2025/9/16 16:43
    IDE: PyCharm
"""
import os.path as op

import matplotlib.pyplot as plt
import numpy as np

from dipy.data import fetch_hbn, get_two_hcp842_bundles
from dipy.io.image import load_nifti
from dipy.io.streamline import load_trk
from dipy.segment.clustering import QuickBundles
from dipy.segment.featurespeed import ResampleFeature
from dipy.segment.metricspeed import AveragePointwiseEuclideanMetric
import dipy.stats.analysis as dsa
import dipy.tracking.streamline as dts


def main():
    subject = "NDARAA948VFH"
    session = "HBNsiteRU"

    fdict, path = fetch_hbn([subject], include_afq=True)

    afq_path = op.join(path, "derivatives", "afq", f"sub-{subject}", f"ses-{session}")

    cst_l_file = op.join(
        afq_path,
        "clean_bundles",
        f"sub-{subject}_ses-{session}_acq-64dir_space-T1w_desc-preproc_dwi_space"
        "-RASMM_model-CSD_desc-prob-afq-CST_L_tractography.trk",
    )

    arc_l_file = op.join(
        afq_path,
        "clean_bundles",
        f"sub-{subject}_ses-{session}_acq-64dir_space-T1w_desc-preproc_dwi_space"
        "-RASMM_model-CSD_desc-prob-afq-ARC_L_tractography.trk",
    )

    cst_l = load_trk(cst_l_file, reference="same", bbox_valid_check=False).streamlines
    arc_l = load_trk(arc_l_file, reference="same", bbox_valid_check=False).streamlines

    model_arc_l_file, model_cst_l_file = get_two_hcp842_bundles()

    model_arc_l = load_trk(
        model_arc_l_file, reference="same", bbox_valid_check=False
    ).streamlines
    model_cst_l = load_trk(
        model_cst_l_file, reference="same", bbox_valid_check=False
    ).streamlines

    feature = ResampleFeature(nb_points=100)
    metric = AveragePointwiseEuclideanMetric(feature)

    qb = QuickBundles(threshold=np.inf, metric=metric)

    cluster_cst_l = qb.cluster(model_cst_l)
    standard_cst_l = cluster_cst_l.centroids[0]

    cluster_af_l = qb.cluster(model_arc_l)
    standard_af_l = cluster_af_l.centroids[0]

    oriented_cst_l = dts.orient_by_streamline(cst_l, standard_cst_l)
    oriented_arc_l = dts.orient_by_streamline(arc_l, standard_af_l)

    fa, fa_affine = load_nifti(
        op.join(
            afq_path,
            f"sub-{subject}_ses-{session}_acq-64dir_space-T1w_desc"
            "-preproc_dwi_model-DTI_FA.nii.gz",
        )
    )

    w_cst_l = dsa.gaussian_weights(oriented_cst_l)
    w_arc_l = dsa.gaussian_weights(oriented_arc_l)

    profile_cst_l = dsa.afq_profile(fa, oriented_cst_l, affine=fa_affine, weights=w_cst_l)

    profile_af_l = dsa.afq_profile(fa, oriented_arc_l, affine=fa_affine, weights=w_arc_l)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot(profile_cst_l)
    ax1.set_ylabel("Fractional anisotropy")
    ax1.set_xlabel("Node along CST")
    ax2.plot(profile_af_l)
    ax2.set_xlabel("Node along ARC")
    fig.savefig("tract_profiles")


    pass


if __name__ == '__main__':
    main()
