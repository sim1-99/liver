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


def main(input_vol, ground_truth=None):
    """
    Implement one-seed based region growing for the extraction of the liver.

    Parameters
    ----------
    input_vol : SimpleITK image
        stack of images to segment
    ground_truth : SimpleITK image, optional
        stack of ground truth segmentation images; the default is None

    Returns
    -------
    rg_mask : SimpleITK image
        stack of segmented images

    """
    # TODO: create pipeline for mask
    # keep only the right part of the CT, because it's where the liver is
    # mostly located
    vol = pp.crop_right_half(input_vol)
    vol = pp.mean_filter(vol, 2)
    vol = pp.threshold(vol, 130, 60, 1, 0)  # empirically chosen values

    slice_of_the_largest_mask = mt.find_biggest_mask(vol)
    x_centroid, y_centroid = mt.find_centroid(vol, slice_of_the_largest_mask)
    centroid = [x_centroid, y_centroid, slice_of_the_largest_mask]

    # TODO: to remove, just for development purpose
    if ground_truth:
        plt_show(ground_truth, centroid)
    print(centroid)

    # TODO: add low pass filter?
    vol = pp.mean_filter(input_vol, 2)
    vol = pp.sigmoid_filter(vol, slice_of_the_largest_mask, centroid)
    vol = pp.histogram_equalization(vol)  # FIX: is it useful?

    rg_mask = mt.region_growing(
        vol, centroid, multiplier=2.5, initialNeighborhoodRadius=2)

    rg_mask = pp.binary_opening(rg_mask, radius=2)
    rg_mask = pp.binary_closing_br(rg_mask, radius=10)
    rg_mask = pp.binary_closing(rg_mask, radius=3)

    return rg_mask
