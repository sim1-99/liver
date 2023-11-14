#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__main__.py for CL application."""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'

import argparse
from LiverExtraction.modules.utils import read_zipped_nifti, write_volume
from LiverExtraction import one_seed_rg
from LiverExtraction import multi_seed_rg


def parse_args():
    """
    Argument parser for the input and output file names.

    Returns
    -------
    args :
        input_arch : str
            name of the .zip archive
        input_file : str
            name of the file inside the .zip archive
        output : str
            name to give to the output file

    """
    description = 'Liver Extraction'
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(help='possible actions',
                                       dest='subparser')

    osrg = subparsers.add_parser('osrg', help='one seed region growing')
    osrg.add_argument('--input_archive',
                      dest='input_arch',
                      required=True,
                      type=str,
                      action='store',
                      help='input archive name')
    osrg.add_argument('--input_file',
                      dest='input_file',
                      required=True,
                      type=str,
                      action='store',
                      help='input file name')
    osrg.add_argument('--output',
                      dest='output',
                      required=True,
                      type=str,
                      action='store',
                      help='output file name')

    msrg = subparsers.add_parser('msrg', help='multiple seeds region growing')
    msrg.add_argument('--input_archive',
                      dest='input_arch',
                      required=True,
                      type=str,
                      action='store',
                      help='input archive name')
    msrg.add_argument('--input_file',
                      dest='input_file',
                      required=True,
                      type=str,
                      action='store',
                      help='input file name')
    msrg.add_argument('--output',
                      dest='output',
                      required=True,
                      type=str,
                      action='store',
                      help='output file name')

    args = parser.parse_args()
    return args


def main():
    """Run the script chosen by the user."""
    args = parse_args()

    if args.subparser == 'osrg':
        one_seed_rg.main(args)
    if args.subparser == 'msrg':
        multi_seed_rg.main(args)
    # write_volume(image=labels, output_filename=args.output)


if __name__ == '__main__':
    main()
