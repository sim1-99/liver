#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__main__.py for CL application."""

__author__ = 'Simone Chiarella'
__email__ = 'simone.chiarella@studio.unibo.it'

import argparse
from LiverExtraction.modules.utils import read_zipped_nifti, write_volume
from LiverExtraction.modules.evaluate import evaluate, print_evaluate
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
    osrg.add_argument('-sb', '--save_binary',
                      action='store_true',
                      help='save also the binary segmentation')

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
    msrg.add_argument('-sb', '--save_binary',
                      action='store_true',
                      help='save also the binary segmentation')

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
        seg_volume, seg_binary, _ = one_seed_rg.main(
            input_volume, ground_truth)
    if args.subparser == 'msrg':
        seg_volume, _, slice_where_to_pick_seeds = one_seed_rg.main(
            input_volume, ground_truth)
        seg_volume, seg_binary = multi_seed_rg.main(
            input_volume, seg_volume, slice_where_to_pick_seeds)

    if args.ground_truth is not None:
        params = evaluate(seg_binary, ground_truth)
        print_evaluate(params)

    write_volume(img=seg_volume, output_file_name=args.output)
    if args.save_binary is True:
        write_volume(
            img=seg_binary, output_file_name=args.output,
            save_binary=args.save_binary)


if __name__ == '__main__':
    main()
