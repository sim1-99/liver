#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multiple-seed based region growing algorithm.

This script imports the CT volume and a the segmentation returned from
one_seed_rg.py. Starting from it, the script picks random pixels inside the
liver segmentation that are used as initial seeds for a region growing
algorithm. This procedure is aimed at extracting the liver. Finally, the
script saves the segmentation in the desired format.
"""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'

import LiverExtraction.modules.preprocessing as pp
import LiverExtraction.modules.methods as mt
from LiverExtraction.modules.utils import plt_show


def main(input_volume, segmentation, slice_where_to_pick_seeds: int):
    """
    Perform multiple-seed based region growing for extracting the liver.

    Parameters
    ----------
    input_volume : SimpleITK image
        stack of images to segment
    segmentation : SimpleITK image
        stack of segmentation images from one_seed_rg.py to use for selecting
        the initial seeds for the region growing algorithm
    slice_where_to_pick_seeds : int
        value representing the slice of the volume where to pick the pixels to
        use as initial seeds for the region growing algorithm

    Returns
    -------
    seg_volume : SimpleITK image
        segmented CT volume
    rg_seg : SimpleITK image
        segmentation mask of the CT volume

    """
    vol = pp.mean_filter(input_volume, radius=3)
    vol = pp.mask_filter(vol, segmentation)

    # FIXME: sigmoid or histogram eq?
    # vol = sigmoid_filter()
    vol = pp.histogram_equalization(vol)

    segmentation_slice = segmentation[:, :, slice_where_to_pick_seeds]
    # FIXME: is the number of iters adequate?
    segmentation_slice = pp.erode(segmentation_slice, radius=1, iters=3)

    number_of_pixels = 30
    x_pixels, y_pixels, liver_conn_comp = mt.pick_random_pixels(
        segmentation_slice, number_of_pixels)

    pixel_coords = [x_pixels, y_pixels, slice_where_to_pick_seeds]
    seed_list = mt.create_seed_list(pixel_coords, number_of_pixels)

    # TODO: visualize just for development purpose
    plt_show(liver_conn_comp)
    plt_show(input_volume, pixel_coords)

    rg_seg = mt.region_growing(
        vol, seed_list, multiplier=2.5, initialNeighborhoodRadius=0)
    rg_seg = pp.binary_opening(rg_seg, radius=2)

    seg_volume = pp.mask_filter(input_volume, rg_seg)

    return (seg_volume, rg_seg)
