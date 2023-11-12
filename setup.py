#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""setup.py file for CL application."""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'

from setuptools import setup

setup(
    name='LiverExtraction',
    version='0.1.0',
    packages=['LiverExtraction'],
    # install_requires = ["required_package", ],
    entry_points={
        'console_scripts': [
            'LiverExtraction = LiverExtraction.__main__:main',
        ]
    })
