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


def write_volume(img, output_file_name):
    """
    Write the image in any format supported by SimpleITK.

    Parameters
    ----------
    img : SimpleITk image file
        image to write
    output_file_name : str
        name to give to the output file

    Example
    -------
    >>> from CTLungSeg.utils import read_image, write_volume
    >>>
    >>> input_file = 'path/ti/input/image'
    >>> image = read_image(input_file)
    >>> # process the image
    >>> # write the image as nrrd
    >>> output_name = 'path/to/output/filename.nrrd'
    >>> write_volume(image, output_name)
    >>> #or write the image as nifti
    >>>  output_name = 'path/to/output/filename.nii'
    >>> write_volume(image, output_name)
    """
    writer = sitk.ImageFileWriter()
    writer.SetFileName(output_file_name)
    writer.Execute(image)
    
    
