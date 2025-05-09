#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 18:27:13 2025

@author: jessicakelly
"""


""" Pandas Solution
import pandas as pd


df = pd.read_csv('Example.hs_intervals.txt', sep='\s+')

df['%gc'] = df['%gc']*100
df['%gc_bin'] = pd.cut(df['%gc'], range(0, 110, 10))

print(df.groupby('%gc_bin')['mean_coverage'].mean().to_frame())
"""


import math


bins = [-1] * 10
bins_count = [0] * 10

for line in open('./Example.hs_intervals.txt', "r").readlines()[1:]:
    line  = line.strip().split()
    perc_gc = float(line[5])*100
    mean_cov = float(line[6])
    
    bin_int = math.floor(perc_gc / 10)
    
    if bins[bin_int] > -1:
        bins[bin_int] += mean_cov
    else:
        bins[bin_int] = mean_cov

        
    bins_count[bin_int] += 1


print("mean coverage per GC content bin:")

for i in range(0, 10):
    bin_total = bins[i]
    if bin_total != -1:
        j = 10*i
        print(f'[{j}-{j+10})% GC: {round(bins[i]/bins_count[i], 3)}')

    