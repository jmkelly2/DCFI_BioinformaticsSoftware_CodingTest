#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  8 17:50:43 2025

@author: jessicakelly
"""

import os
import sys
from collections import Counter


input_fasta = sys.argv[1]
#input_fasta = './sample_files/fasta/sample.fasta'


sequences = []
max_count = 0

def parse_fasta(filepath):
    for line in open(filepath, 'r').readlines()[1::2]:
        sequences.append(line.strip())
        
    return sequences

    
most_freq_seq = Counter(parse_fasta(input_fasta)).most_common(1)
print(f'The most frequent sequence is {most_freq_seq[0][0]}.')
print(f'It occurs {most_freq_seq[0][1]} times.')
