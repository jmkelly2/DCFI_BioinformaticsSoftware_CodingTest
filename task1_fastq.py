#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 10:12:00 2025

@author: kellyjes
"""

import os
import sys

input_directory = sys.argv[1]


def report_seq_g_30nt(fastq):
    greater30 = 0
    total = 0

    for line in open(fastq, "r").readlines()[1::4]:
        length = len(line.strip())
        if length > 30:
            greater30 += 1
        total += 1
        
    return(round(100*greater30/total, 3))



def find_fastq(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.fastq'):
                fastq_path = os.path.join(root, file)
                print(f'{fastq_path}: {report_seq_g_30nt(fastq_path)}%')
                
                
find_fastq(input_directory)
    
