#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  8 17:50:43 2025

@author: Jessica Kelly

usage: task1_fasta.py [path/file.fasta]
"""

import argparse


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
    
    seq_counts = {} #initialize dictionary
    
    for line in open(filepath, 'r').readlines():
        
        line = line.strip() #remove newline char
        
        if not line.startswith(">"):
            #skip header lines, increment count at dict seq key
            
            seq_counts[line] = seq_counts.get(line, 0) + 1

    
    #return maximum dictionary count entry (seq, count)
    return max(seq_counts.items(), key=lambda entry: entry[1])


def main():
    """ main method to most frequent sequence in fastq"""
    
    input_fasta = get_cli_args().fasta_filepath
    
    most_freq_seq, count = get_most_freq_seq(input_fasta)
    
    print(f'\n The most frequent sequence is {most_freq_seq}.')
    print(f'It occurs {count} times.\n')


if __name__ == '__main__':
    main()
