#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 10:12:00 2025

@author: Jessica Kelly

usage: python task1_fastq.py [path/file.fastq]
purpose: recursively find fastq files in a directory
    and report the % sequences in the fastq with greater than 30 nt
"""

import os
import sys
import argparse


def get_cli_args():
    """
    Get the command line options using argparse
    @return: Instance of argparse arguments
    """

    parser = argparse.ArgumentParser(description="Give fastq file directory")
    parser.add_argument('fastq_directory')

    return parser.parse_args()


def check_valid_directory(directory):
    """" method to validate that input directory exists """

    if not os.path.isdir(directory):
        print("Not found")
        print(f"Error: {directory} does not exist. Exiting now...",
          file=sys.stderr)
        sys.exit(1)


def check_valid_fastq(seq, fastq, total):
    """ method to validate fastq format """

    if not seq.startswith(('A', 'T', 'G', 'C', 'N', '\n')):
        print(f"Posssible formatting error at sequence {total} in {fastq}")
        print(seq.strip())
        print("Warning: Check sequence printed above for formatting issues.\n")


def report_seq_g_30nt(fastq):
    """
    Parse fastq and count length of sequences
    @return: percent sequences > 30 nt
    """

    greater30 = 0
    total = 0

    for line in open(fastq, "r").readlines()[1::4]:
        #fastq have 4 lines of annotation
        #second line and every 4th represent sequence
        check_valid_fastq(line, fastq, total)

        length = len(line.strip()) #remove newline char

        if length > 30:
            greater30 += 1

        total += 1 #keep track of seq in file

    return(round(100*greater30/total, 3))


def find_fastq(directory):
    """
    Recursively search for fastq and call function to report seq > 30 nt
    @return: list of strings reporting fastq files and their % seq > 30 nt
    """

    results = []
    for root, dirs, files in os.walk(directory):
        #recursively search directory

        for file in files:
            if file.endswith('.fastq'):
                #files with fastq extension

                fastq_path = os.path.join(root, file) #full file path
                results.append(f"{fastq_path}: {report_seq_g_30nt(fastq_path)}%")

    return results
                
                
def main():
    """ main method to report percent percent seq greater than 30 nt in fastq file"""

    input_directory = get_cli_args().fastq_directory
    check_valid_directory(input_directory)
    report = find_fastq(input_directory)

    if report != []:
        #check that there were fastq files found

        print("\nReporting % sequences with > 30 nt per fastq file found:")

        for r in report:
            print(r)
        print('\n')

    else:
        print("Warning: No fastq files found in directory!", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
