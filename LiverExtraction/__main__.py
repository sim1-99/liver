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

    subparsers = parser.add_subparsers(
        dest='subparser', help='possible actions')

    osrg = subparsers.add_parser('osrg', help='one-seed based region growing')
    # positional arguments
    osrg.add_argument('input_archive',
                      required=True, type=str,
                      help='name of the input archive')
    osrg.add_argument('input_file',
                      required=True, type=str,
                      help='name of the input file')
    osrg.add_argument('output',
                      required=True, type=str,
                      help='name of the output file')
    # optional arguments
    osrg.add_argument('-gt', '--ground_truth',
                      action='append', nargs=2, type='str',
                      help='name of the ground truth segmentation archive and '
                      'file')

    msrg = subparsers.add_parser(
        'msrg', help='multiple-seeds based region growing')
    # positional arguments
    msrg.add_argument('input_archive',
                      required=True, type=str,
                      help='name of the input archive')
    msrg.add_argument('input_file',
                      required=True, type=str,
                      help='name of the input file')
    msrg.add_argument('output',
                      required=True, type=str,
                      help='name of the output file')
    # optional arguments
    msrg.add_argument('-gt', '--ground_truth',
                      action='append', nargs=2, type='str',
                      help='name of the ground truth segmentation archive and '
                      'file')

    args = parser.parse_args()
    return args


def main():
    """Run the script chosen by the user."""
    args = parse_args()
    input_volume = read_zipped_nifti(archive_name=args.input_archive,
                                     file_name=args.input_file)

    if args.ground_truth is not None:
        ground_truth = read_zipped_nifti(archive_name=args.ground_truth[0],
                                         file_name=args.ground_truth[1])

    if args.subparser == 'osrg':
        segmentation, _ = one_seed_rg.main(input_volume, ground_truth)
    if args.subparser == 'msrg':
        segmentation, slice_where_to_pick_seeds = one_seed_rg.main(
            input_volume, ground_truth)
        segmentation = multi_seed_rg.main(
            input_volume, segmentation, slice_where_to_pick_seeds)

    write_volume(img=segmentation, output_file_name=args.output)


if __name__ == '__main__':
    main()
