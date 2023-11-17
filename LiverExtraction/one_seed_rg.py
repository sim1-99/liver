#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-seed based region growing algorithm.

This script imports the CT volume, makes some preprocessing and performs a
region growing operation starting from one seed to extract the liver. Then
saves the segmentation in the desired format.
"""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'

import LiverExtraction.modules.preprocessing as pp
import LiverExtraction.modules.methods as mt
from LiverExtraction.modules.utils import plt_show


def main(input_volume, ground_truth=None):
    """
    Perform one-seed based region growing for extracting the liver.

    Parameters
    ----------
    input_volume : SimpleITK image
        stack of images to segment
    ground_truth : SimpleITK image, optional
        stack of ground truth segmentation images; the default is None

    Returns
    -------
    rg_seg : SimpleITK image
        stack of segmented images
    slice_of_the_largest_mask: int
        index referring to the slice of the volume to use in multi_seed_rg.py

    """
    # keep only the right part of the CT, because it's where the liver is
    # mostly located
    vol = pp.crop_right_half(input_volume)
    vol = pp.mean_filter(vol, 2)
    vol = pp.threshold(vol, 130, 60, 1, 0)  # empirically chosen values

    slice_of_the_largest_mask = mt.find_biggest_mask(vol)
    x_centroid, y_centroid = mt.find_centroid(vol, slice_of_the_largest_mask)
    centroid = [x_centroid, y_centroid, slice_of_the_largest_mask]

    # TODO: visualize just for development purpose
    if ground_truth:
        plt_show(ground_truth, centroid)
    print(centroid)

    # TODO: add low pass filter?
    vol = pp.mean_filter(input_volume, 2)
    vol = pp.sigmoid_filter(vol, slice_of_the_largest_mask, centroid)
    vol = pp.histogram_equalization(vol)  # FIX: is it useful?

    rg_seg = mt.region_growing(
        vol, centroid, multiplier=2.5, initialNeighborhoodRadius=2)
    rg_seg = pp.binary_opening(rg_seg, radius=2)
    rg_seg = pp.binary_closing_br(rg_seg, radius=10)
    rg_seg = pp.binary_closing(rg_seg, radius=3)

    return (rg_seg, slice_of_the_largest_mask)
