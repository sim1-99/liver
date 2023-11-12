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


def find_biggest_mask(img) -> int:
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
    biggest_mask_slice_idx : int
        value indicating the slice of the input volume having the largest
        number of foreground pixels

    """
    num_slices = int(len(img)/len(img[:, :, 0]))
    biggest_mask_area = 0
    biggest_mask_slice_idx = 0
    for slice in range(num_slices):
        np_img = sitk.GetArrayFromImage(img)[slice, :, :]
        if (np.count_nonzero(np_img) > biggest_mask_area):
            biggest_mask_area = np.count_nonzero(np_img)
            biggest_mask_slice_idx = slice
    return biggest_mask_slice_idx


def find_centroid(img, mask, slice_idx: int) -> (int, int):
    """
    Find the centroid of the liver connected component.

    This function is used to pick the centroid of the liver connected
    component, in the slice of the input volume having the largest number of
    foreground pixels. This pixel will be later used as the initial seed for a
    region growing algorithm.

    Parameters
    ----------
    img : SimpleITK image
        stack of thresholded images
    mask : SimpleITK image              # FIXME: just for development purpose
        stack of ground truth images
    slice_idx : int
        value indicating one slice of the input volume

    Returns
    -------
    x_centroid : int
        x-coordinate of the centroid of the liver connected component
    y_centroid : int
        y-coordinate of the centroid of the liver connected component

    """
    output = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output

    liver_label = np.argsort(np.max(stats, axis=1))[-2]

    x_centroid = centroids[liver_label][0]
    y_centroid = centroids[liver_label][1]

    # FIXME: remove the following 4 lines when no need of visualizing
    plt.figure(figsize=(8, 8))
    plt.imshow(sitk.GetArrayFromImage(mask)[slice_idx, :, :], cmap='gray')
    plt.scatter(x_centroid, y_centroid, s=30, c='red', marker='o')
    plt.show()

    x_centroid = np.uint32(x_centroid).item()
    y_centroid = np.uint32(y_centroid).item()

    return (x_centroid, y_centroid)


def region_growing(img, seed: list, multiplier: float, radius: int,
                   iters: int = 0):
    """
    Region growing algorithm based on the function sitk.ConfidenceConnected.

    From the documentation of sitk.ConfidenceConnected (up to 07/11/2023):

    << This filter extracts a connected set of pixels whose pixel intensities
    are consistent with the pixel statistics of a seed point. The mean and
    variance across a neighborhood (8-connected, 26-connected, etc.) are
    calculated for a seed point. Then pixels connected to this seed point whose
    values are within the confidence interval for the seed point are groped.
    The width of the confidence interval is controlled by the "Multiplier"
    variable (the confidence interval is the mean plus or minus the
    "Multiplier" times the standard deviation). [...] After this initial
    segmentation is calculated, the mean and variance are re-calculated. All
    the pixels in the previous segmentation are used to calculate the mean and
    the standard deviation (as opposed to using the pixels in the neighborhood
    of the seed point). The segmentation is then recalculated using these
    refined estimates for the mean and variance of the pixel values. This
    process is repeated for the specified number of iterations. Setting the
    "NumberOfIterations" to zero stops the algorithm after the initial
    segmentation from the seed point. >>

    Parameters
    ----------
    img : SimpleITK image
        stack of images
    seed : list
        x-, y- and z-coordinates of the initial seed or seeds
    multiplier : float
        value controlling the width of the confidence interval that determines
        the connectivity between pixels; a classical value is 2.5
    radius : int
        initial neighbourhood radius, must be greater than or equal to 1
    iters : int, optional
        maximum number of iterations to run the algorithm; the default is 0

    Returns
    -------
    connectivity_mask : SimpleITK image
        stack of images

    """
    connectivity_mask = sitk.ConfidenceConnected(
        img, seedList=seed, numberOfIterations=iters,
        multiplier=multiplier, initialNeighborhoodRadius=radius)
    return sitk.Cast(connectivity_mask, sitk.sitkUInt8)


def pick_random_pixels(img, slice_idx: int, number_of_pixels: int
                       ) -> (np.ndarray, np.ndarray):
    """
    Pick random pixels from a slice.

    This function is used to pick a variable number of random pixels in the
    slice of the input volume specified by 'slice_idx'. Those pixels will be
    successively used as initial seeds for the region growing algorithm.

    Parameters
    ----------
    img : SimpleITK image
        stack of binary images
    slice_idx : int
        value indicating one slice of the input volume
    number_of_pixels : int
        number of random pixels to pick

    Returns
    -------
    x_pixels : np.ndarray
        x-coordinates of the picked pixels
    y_pixels : np.ndarray
        y-coordinates of the picked pixels

    """
    img = sitk.GetArrayFromImage(img)

    output = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output

    liver_label = np.argsort(np.max(stats, axis=1))[-2]
    component = np.where(labels == liver_label, 1, 0)
    non_zero_pixels = np.asarray(np.nonzero(component))
    rng = np.random.default_rng(seed=9)
    random_idx = rng.choice(np.arange(non_zero_pixels.shape[1]),
                            number_of_pixels, replace=False, shuffle=False)
    x_pixels = non_zero_pixels[1, random_idx]
    y_pixels = non_zero_pixels[0, random_idx]

    plt.imshow(component, cmap='gray')  # FIXME: for development purpose,
    #                                            to be removed

    return (x_pixels, y_pixels)


def create_seed_list(x_pixels: np.ndarray, y_pixels: np.ndarray,
                     slice_idx: int, number_of_pixels: int
                     ) -> list:
    """
    Reshape the output of pick_random_pixels into the form of a seed list.

    Parameters
    ----------
    x_pixels : np.ndarray
        x-coordinates of the picked pixels
    y_pixels : np.ndarray
        y-coordinates of the picked pixels
    slice_idx : int
        value indicating one slice of the input volume; it must be the same
        passed to pick_random_pixels
    number_of_pixels : int
        number of random pixels to pick; it must be the same passed to
        pick_random_pixels

    Returns
    -------
    seed_list : list
        list of pixels to be used as region growing initial seeds

    """
    x_pixels = x_pixels.reshape(number_of_pixels, 1)
    y_pixels = y_pixels.reshape(number_of_pixels, 1)
    seed_slice = np.repeat(
        slice_idx, number_of_pixels).reshape(number_of_pixels, 1)

    seed_list = np.concatenate([x_pixels, y_pixels, seed_slice], axis=1)
    return seed_list.tolist()
