#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 18:27:13 2025

@author: jessicakelly
"""

""" Pandas Solution. This solution is simple, but doesn't show off too many skills
import pandas as pd


df = pd.read_csv('Example.hs_intervals.txt', sep='\s+')

df['%gc'] = df['%gc']*100
df['%gc_bin'] = pd.cut(df['%gc'], range(0, 110, 10))

print(df.groupby('%gc_bin')['mean_coverage'].mean().to_frame())
"""


import argparse
import math


def get_cli_args():
    """
    Get the command line options using argparse
    @return: Instance of argparse arguments
    """

    parser = argparse.ArgumentParser(description="Give fasta file path")
    parser.add_argument('-i',
                        dest='interval_file',
                        type=str,
                        default="./Example.hs_intervals.txt")

    return parser.parse_args()


def make_binned_coverage(interval_file):
    """
    Parse interval file and bin according to %GC.
    Sum mean coverages per bin and keep track of how many intervals per bin
    @return: list of summed mean coverage per bin
    @return: list of total number of intervals per bin
    """
    
    #initialize bins to keep track of bin interval count and total mean coverage
    #bin index represent 10's place of GC% (ex: bin[0] is intervals with 0-10%GC, bin[9] is 90-100%GC)
    binned_coverage = [-1] * 10
    binned_counts = [0] * 10
    
    for line in open(interval_file, "r").readlines()[1:]:
        #skip first line - header
        
        #parse line to get percent gc and mean coverage columns
        line = line.strip().split()
        perc_gc = float(line[5])*100 #make out of 100% instead decimal
        mean_cov = float(line[6])
        
        #get 10s place of percent GC to define bin index
        bin_index = math.floor(perc_gc / 10)
        
        #add mean coverage to coverage sum of bin
        if binned_coverage[bin_index] > -1:
            binned_coverage[bin_index] += mean_cov
        else:
            #initialize bin coverage
            binned_coverage[bin_index] = mean_cov
    
        binned_counts[bin_index] += 1 #increment count of intervals in bin
        
    return binned_coverage, binned_counts


def report_binned_mean_coverage(binned_coverage, binned_counts):
    """ Calculate average per bin and report output """
    
    print("\nMean coverage per GC content bin:\n")
    
    for i in range(0, 10):
        bin_total = binned_coverage[i]

        if bin_total != -1:
            #only report for bins which had intervals

            j = 10*i #lower bound %GC is bin index*10 (ex: bin[9] is 90-100%GC)

            #sum bin coverage / count intervals in bin = mean bin coverage
            mean_bin_cov = bin_total/binned_counts[i]

            print(f'[{j}-{j+10})% GC: {round(mean_bin_cov, 3)}')
            
    print("\n")


def main():
    """ main method to assess mean coverage across gc binned_coverage"""
    
    interval_file = get_cli_args().interval_file
    
    total_coverage, count_intervals = make_binned_coverage(interval_file)
    report_binned_mean_coverage(total_coverage, count_intervals)
    

if __name__ == '__main__':
    main()
