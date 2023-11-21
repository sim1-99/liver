#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utils.

This module contains a set of funtions used for file management (e.g.,
for reading and saving files).
"""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'

from pathlib import Path
import zipfile
import shutil
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt


def read_zipped_nifti(archive_name: str, file_name: str):
    """
    Read .nii files from a .zip archive.

    The path to the files must be:

    . > liver > archive.zip > file.nii

    Parameters
    ----------
    archive_name : str
        name of the .zip archive
    file_name : str
        name of the file to read

    Returns
    -------
    file: SimpleITK image
        stack of images to read

    """
    temp_dir = Path.home()/'liver'/'temp'
    myzip_path = Path.home()/'liver'/archive_name

    with zipfile.ZipFile(myzip_path) as myzip:
        myzip.extract(file_name, path=temp_dir)
    file = sitk.ReadImage(temp_dir/file_name, imageIO='NiftiImageIO')
    shutil.rmtree(temp_dir)

    return file


def plt_show(img, pixel_coord: list = None) -> None:
    """
    Show NumPy arrays and SimpleITK images using Matplotlib.

    Parameters
    ----------
    img : np.ndarray or SimpleITK image
        image or stack of images to visualize
    pixel_coord : list, optional
        list containing the coordinates of possible points to display on the
        image; the default is None

    Returns
    -------
    None

    """
    if pixel_coord is None:
        if img is np.ndarray:
            plt.imshow(img, cmap='gray')
        else:
            plt.imshow(sitk.GetArrayFromImage(img), cmap='gray')
    elif img.GetDimension() == 3:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
        plt.imshow(
            sitk.GetArrayFromImage(img)[pixel_coord[2], :, :], cmap='gray')
        plt.scatter(
            pixel_coord[0], pixel_coord[1], s=30, c='red', marker='o')
        plt.show()


def write_volume(img, output_file_name, save_binary=False) -> None:
    """
    Write the image in any format supported by SimpleITK.

    If save_binary is set to True, then the indication '_binary' is added to
    the file name before the file format.

    Parameters
    ----------
    img : SimpleITk image file
        image to write
    output_file_name : str
        name to give to the output file
    save_binary : bool, optional
        if True, the string '_binary' is added to the file name before the
        file format; the default is False

    Returns
    -------
    None

    """
    writer = sitk.ImageFileWriter()
    if save_binary is True:
        file_name = output_file_name.split('.')[0]
        file_format = output_file_name.split('.')[1]
        writer.SetFileName(file_name+'_binary'+file_format)
    else:
        writer.SetFileName(output_file_name)
    writer.Execute(img)
