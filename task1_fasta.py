#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  8 17:50:43 2025

@author: Jessica Kelly

usage: task1_fasta.py [path/file.fasta]
purpose: find top 10 most frequent DNA sequences in a FASTA file
"""

import argparse
from collections import defaultdict


def get_cli_args():
    """
    Get the command line options using argparse
    @return: Instance of argparse arguments
    """

    parser = argparse.ArgumentParser(description="Give fasta file path")
    parser.add_argument('fasta_filepath')

    return parser.parse_args()


def get_most_freq_seq(filepath):
    """
    Parse fasta and track counts of sequence occurence
    @return: most common sequence and its count
    """

    seq_counts = defaultdict(int) #initialize dictionary to count from 0

    for line in open(filepath, 'r').readlines():

        line = line.strip() #remove newline char

        if not line.startswith(">"):
            #skip header lines, increment count at dict seq key

            seq_counts[line] += 1

    #return top 10 highest count entries (seq, count)
    return sorted(seq_counts.items(), key=lambda entry: entry[1], reverse=True)[:10]


def report_top10_seq(seqs):
    """ Report top 10 most frequent seqs and their counts to out"""

    print("\nTop 10 Most Frequent Sequences in Fasta:\n")
    print(" Count\tSequence")

    i = 1
    for item in seqs:
        print(f"{i}.  {item[1]}\t{item[0]}")
        i+=1


def main():
    """ main method to most frequent sequences in fasta"""

    input_fasta = get_cli_args().fasta_filepath

    most_freq = get_most_freq_seq(input_fasta)

    report_top10_seq(most_freq)


if __name__ == '__main__':
    main()
