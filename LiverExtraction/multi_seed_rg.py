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


import numpy as np
import SimpleITK as sitk

from LiverExtraction.modules.utils import write_volume


def main(img):
    return 0
