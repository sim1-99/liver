#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preprocessing.

This module contains a set of funtions for the preprocessing of the CT volumes.
"""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'

import SimpleITK as sitk
import numpy as np


def binary_closing(img, radius: int):
    """
    Morphological closing.

    Perform morphological closing (i.e., dilation followed by erosion) on a
    binary image.

    Parameters
    ----------
    img : SimpleITK image
        binary image or stack of images to close
    radius : int
        neighbourhood radius, must be greater than or equal to 1

    Returns
    -------
    img : SimpleITK image
        closed image or stack of images

    Raises
    ------
    ValueError
        if the input image is the radius is smaller than 1

    """
    filter = sitk.BinaryMorphologicalClosingImageFilter()
    if radius <= 0:
        raise ValueError('Radius must be greater than or equal to 1.')
    filter.SetKernelType(sitk.sitkBall)
    filter.SetKernelRadius(int(radius))

    return filter.Execute(img)


def binary_closing_br(img, radius: int):
    """
    Morphological closing by reconstruction.

    Perform morphological closing (i.e., dilation followed by erosion) on a
    binary image, but preserve the shape of bigger objects.

    Parameters
    ----------
    img : SimpleITK image
        binary image or stack of images to close
    radius : int
        neighbourhood radius, must be greater than or equal to 1

    Returns
    -------
    img : SimpleITK image
        closed image or stack of images

    Raises
    ------
    ValueError
        if the input image is the radius is smaller than 1

    """
    filter = sitk.BinaryClosingByReconstructionImageFilter()
    if radius <= 0:
        raise ValueError('Radius must be greater than or equal to 1.')
    filter.SetKernelType(sitk.sitkBall)
    filter.SetKernelRadius(int(radius))

    return filter.Execute(img)


def binary_opening(img, radius: int):
    """
    Morphological opening.

    Perform morphological opening (i.e., erosion followed by dilation) on a
    binary image.

    Parameters
    ----------
    img : SimpleITK image
        binary image or stack of images to open
    radius : int
        neighbourhood radius, must be greater than or equal to 1

    Returns
    -------
    img : SimpleITK image
        opened image or stack of images

    Raises
    ------
    ValueError
        if the input image is the radius is smaller than 1

    """
    filter = sitk.BinaryMorphologicalOpeningImageFilter()
    if radius <= 0:
        raise ValueError('Radius must be greater than or equal to 1.')
    filter.SetKernelType(sitk.sitkBall)
    filter.SetKernelRadius(int(radius))

    return filter.Execute(img)


def crop_right_half(img):
    """
    Crop the image keeping only its left half.

    Parameters
    ----------
    img : SimpleITK image
        image or stack of images to crop

    Returns
    -------
    img : SimpleITK image
        cropped image or stack of images

    """
    filter = sitk.CropImageFilter()
    if img.GetDimension() == 2:
        filter.SetLowerBoundaryCropSize([0, 0])
        filter.SetUpperBoundaryCropSize([256, 0])
    elif img.GetDimension() == 3:
        filter.SetLowerBoundaryCropSize([0, 0, 0])
        filter.SetUpperBoundaryCropSize([256, 0, 0])

    return filter.Execute(img)


def erode(img, radius: int, iters: int = 1):
    """
    Perform grayscale erosion on the input image.

    Parameters
    ----------
    img : SimpleITK image
        image or stack of images to erode
    radius : int
        neighbourhood radius, must be greater than or equal to 1
    iters : int, optional
        number of interations to run; the default is 1

    Returns
    -------
    img : SimpleITK image
        eroded image or stack of images

    Raises
    ------
    ValueError
        if the input image is the radius is smaller than 1

    """
    filter = sitk.GrayscaleErodeImageFilter()
    if radius <= 0:
        raise ValueError('Radius must be greater than or equal to 1.')
    filter.SetKernelType(sitk.sitkBall)
    filter.SetKernelRadius(int(radius))
    for iter in range(iters):
        img = filter.Execute(img)

    return img


def histogram_equalization(img):
    """
    Perform the histogram equalization of the input image.

    Parameters
    ----------
    img : SimpleITK image
        input image or stack of images to equalize

    Returns
    -------
    img : SimpleITK image
        equalized image or stack of images

    """
    num_slices = int(len(img)/len(img[:, :, 0]))

    # create a ramp image of the same size of the input image
    hist = np.arange(0, 255, 255./512., dtype='f4')
    hist = np.reshape(np.repeat(hist, num_slices*512), (num_slices, 512, 512))
    hist = sitk.GetImageFromArray(hist)
    hist = sitk.Cast(hist, img.GetPixelID())

    # match the histogram of the Gaussian image with the ramp
    return sitk.HistogramMatching(img, hist)


def mask_filter(img, mask):
    """
    Apply the input mask on the input image.

    Parameters
    ----------
    img : SimpleITK image
        image or stack of images to mask
    mask : SimpleITK image
        image or stack of images to mask the image with

    Returns
    -------
    img : SimpleITK image
        masked image or stack of images

    """
    if img.GetDimension() == 2:
        sample_slice = sitk.GetArrayFromImage(img)
    elif img.GetDimension() == 3:
        sample_slice = sitk.GetArrayFromImage(img)[0, :, :]
    # 0 just because the slice is not relevant

    filter = sitk.MaskImageFilter()
    filter.SetMaskingValue(0.)
    filter.SetOutsideValue(np.double(sample_slice.min()).item())

    return filter.Execute(img, mask)


def mean_filter(img, radius: int):
    """
    Apply mean blurring filter on the input image.

    Parameters
    ----------
    img : SimpleITK image
        image or stack of images to filter
    radius : int
        neighbourhood radius, must be greater than or equal to 1

    Returns
    -------
    img : SimpleITK image
        mean blurred image or stack of images

    Raises
    ------
    ValueError
        if the input image is the radius is smaller than 1

    """
    if radius <= 0:
        raise ValueError('Radius must be greater than or equal to 1.')
    filter = sitk.MeanImageFilter()
    filter.SetRadius(int(radius))

    return filter.Execute(img)


def sigmoid_filter(img, slice_idx: int, pixel: list):
    """
    Sigmoid filter.

    This function measures some GL quantities inside a ROI centered around a
    pixel within the liver. Those quantities are used for computing the sigmoid
    function pixel-wise:

        f(x) = (Max−Min) × 1/(1+e^(−(x−α)/β)) + Min,

    in order to improve the contrast between the liver and other anatomical
    structures. Max and Min are the maximum and the minimum GL of the input
    slice, while alpha and beta are calculated from the quantities extracted
    from the ROI.

    Parameters
    ----------
    img : SimpleITK image
        image or stack of images to filter
    slice_idx : int
        value indicating the slice to analyze for calculating the sigmoid
        function
    pixel : list
        list containing the x and y coordinates of the center of the ROI

    Returns
    -------
    img : SimpleITK image
        filtered image or stack of images

    """
    if img.GetDimension() == 2:
        sample_slice = img
    elif img.GetDimension() == 3:
        sample_slice = img[:, :, slice_idx]

    stats = sitk.StatisticsImageFilter()

    stats.Execute(sample_slice)
    input_min = stats.GetMinimum()
    input_max = stats.GetMaximum()

    extract_roi = sitk.RegionOfInterestImageFilter()
    extract_roi.SetIndex(pixel)
    extract_roi.SetSize([20, 20])
    roi = extract_roi.Execute(sample_slice)

    stats.Execute(roi)
    roi_mean = stats.GetMean()
    roi_min = stats.GetMinimum()
    roi_max = stats.GetMaximum()

    alpha = roi_max-roi_min
    beta = roi_mean

    filter = sitk.SigmoidImageFilter()
    filter.SetOutputMinimum(input_min)
    filter.SetOutputMaximum(input_max)
    filter.SetAlpha(alpha)
    filter.SetBeta(beta)

    return filter.Execute(img)


def threshold(img, upper: int, lower: int, inside: int = 1, outside: int = 0):
    """
    Perform interval thresholding on the input image.

    Parameters
    ----------
    img : SimpleITK image
        image or stack of images to threshold
    upper : int
        upper threshold value
    lower : int
        lower threshold value
    inside : int, optional
        value to assign to the voxels with GL in [lower, upper];
        the default is 1
    outside : int, optional
        value to assign to the voxels with GL outside [lower, upper];
        the default is 0

    Returns
    -------
    img : SimpleITK image
        thresholded image or stack of images

    """
    thr = sitk.BinaryThresholdImageFilter()
    thr.SetLowerThreshold(lower)
    thr.SetUpperThreshold(upper)
    thr.SetOutsideValue(outside)
    thr.SetInsideValue(inside)

    return thr.Execute(img)
