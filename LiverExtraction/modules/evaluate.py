#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluate.

This module contains a set of funtions used for evaluating the segmentations.
"""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'

import SimpleITK as sitk
import numpy as np
from medpy.metric.binary import dc, jc, obj_assd


def evaluate(seg, gt) -> (float, float, float, float, float):
    """
    Evaluate the segmentation.

    Calculate the following quantities for the evaluation of the segmenation,
    by comparing it with a ground truth segmentation:
        - volumetric overlap error (VOE)
        - relative volume difference (RVD)
        - Dice coefficient
        - Jaccard index
        - average symmetric surface distance (ASSD)

    Parameters
    ----------
    seg : SimpleITK image
        binary segmentation to evaluate
    gt : SimpleITK image
        binary ground truth segmentation

    Returns
    -------
    (float, float, float, float, float)
        VOE, RVD, Dice coefficient, Jaccard index, ASSD

    """
    gt = gt == 1  # here I choose as ground truth mask only the helthy liver
    # tissues, without tumors
    seg = sitk.GetArrayFromImage(seg)
    gt = sitk.GetArrayFromImage(gt)

    voe = 100 * (
        1.-np.logical_and(seg, gt).sum()/float(np.logical_or(seg, gt).sum()))
    rvd = 100 * abs((float(seg.sum()) - float(gt.sum())) / float(gt.sum()))
    dice = dc(seg, gt)
    jaccard = jc(seg, gt)
    assd = obj_assd(seg, gt)

    voe, assd = np.float64(voe).item(), np.float64(assd).item()

    return (voe, rvd, dice, jaccard, assd)


def print_evaluate(evals) -> None:
    """
    Print the output of evaluate.

    Parameters
    ----------
    evals : list
        evaluation parameters

    Returns
    -------
    None

    """
    print(f"VOE: {evals[0]}"
          f"RVD: {evals[1]}"
          f"Dice coefficient: {evals[2]}"
          f"Jaccard index: {evals[3]}"
          f"ASD: {evals[4]}")
