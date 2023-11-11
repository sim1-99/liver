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


def read_zipped_nifti(file_idx: int):
    """
    Read .nii files from a .zip archive.

    The path to the files must be:

    . > liver > LiTS_data.zip > LiTS_data > volumes       > volume-0.nii
                                          > segmentations > segmentation-0.nii

    TODO: give the possibility to pass from CL a different archive
    TODO: remove the part of the segmentation after development stage

    Parameters
    ----------
    file_idx : int
        index of the file to read

    Returns
    -------
    vol: SimpleITK image
        stack of CT images to read
    seg: SimpleITK image
        stack of segmentation images to read

    """
    temp_dir = Path.home()/'liver'/'temp'
    myzip_path = Path.home()/'liver'/'LiTS_data.zip'

    vol_dir = Path('LiTS_data')/'volumes'
    vol_file_name = 'volume-' + file_idx + '.nii'
    vol_path = vol_dir/vol_file_name
    vol_path = str(vol_path)

    seg_dir = Path('LiTS_data')/'segmentations'
    seg_file_name = 'segmentation-' + file_idx + '.nii'
    seg_path = seg_dir/seg_file_name
    seg_path = str(seg_path)

    with zipfile.ZipFile(myzip_path) as myzip:
        myzip.extract(vol_path, path=temp_dir)
        myzip.extract(seg_path, path=temp_dir)

    vol = sitk.ReadImage(temp_dir/vol_path, imageIO='NiftiImageIO')
    seg = sitk.ReadImage(temp_dir/seg_path, imageIO='NiftiImageIO')

    shutil.rmtree(temp_dir)

    return (vol, seg)
