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


import numpy as np
import SimpleITK as sitk

from LiverExtraction.modules.utils import write_volume


def main(img):
    return 0
