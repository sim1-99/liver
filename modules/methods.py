#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods.

This module contains a set of funtions used in the extaction of the liver from
the CT volumes.
"""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'

import SimpleITK as sitk
import numpy as np
import pylab as plt
import cv2


def find_biggest_mask(img):
    """
    Find the slice in the volume with the largest number of foreground pixels.

    The input must be a thresholded stack of images. The function returns the
    image in the stack having the largest number of foreground pixels. If the
    preliminary thresholding is centered around the typical gray values of the
    liver, the selected image will most likely contain a significant slice of
    the liver.

    Parameters
    ----------
    img : SimpleITK image
        stack of thresholded images

    Returns
    -------
    biggest_mask_slice : int
        value indicating the slice of the input volume having the largest
        number of foreground pixels

    """
    num_slices = int(len(img)/len(img[:, :, 0]))
    biggest_mask_area = 0
    biggest_mask_slice = 0
    for slice in range(num_slices):
        np_img = sitk.GetArrayFromImage(img)[slice, :, :]
        if (np.count_nonzero(np_img) > biggest_mask_area):
            biggest_mask_area = np.count_nonzero(np_img)
            biggest_mask_slice = slice
    return biggest_mask_slice


def find_centroid(img, mask, slice_idx: int) -> (int, int):
    """
    Find the centroid of the liver connected component.

    Parameters
    ----------
    img : SimpleITK image
        stack of thresholded images
    mask : SimpleITK image                 # just for development purpose
        stack of ground truth images
    slice_idx : int
        value indicating the slice of the input volume having the largest
        number of foreground pixels

    Returns
    -------
    x_centroid : int
        x coordinate of the centroid of the liver connected component
    y_centroid : int
        y coordinate of the centroid of the liver connected component

    """
    output = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output

    liver_label = np.argsort(np.max(stats, axis=1))[-2]

    plt.figure(figsize=(8, 8))
    plt.imshow(sitk.GetArrayFromImage(mask)[slice_idx, :, :], cmap='gray')
    x_centroid = centroids[liver_label][0]
    y_centroid = centroids[liver_label][1]
    plt.scatter(x_centroid, y_centroid, s=30, c='red', marker='o')
    plt.show()

    return (x_centroid, y_centroid)
