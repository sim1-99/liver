#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
First region growing.

This script imports the CT volume, performs some preprocessing and a first
region growing on it to extract the liver. Then saves this first segmentation
in a .nii file.
"""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'


import argparse
import numpy as np
import SimpleITK as sitk
