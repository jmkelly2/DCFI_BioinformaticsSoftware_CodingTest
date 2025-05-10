#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  8 19:59:59 2025

@author: Jessica Kelly

usage: python task1_annotations.py --gtf [path/file.gtf] -i [path/file_to_annoate.txt]

Note: I chose to parse the gtf and store only the start and end positions of each gene instead of full annotations,
since it seems that is the information we are looking for here and it imporves teh efficiency of querying.
"""

import argparse
from collections import defaultdict


def get_cli_args():
    """
    Get the command line options using argparse
    @return: Instance of argparse arguments
    """

    parser = argparse.ArgumentParser(description='Give the filepath to gtf and file with chr pos to annotate per line')

    parser.add_argument('--gtf', dest='gtf', type=str,
                        help='gtf annotation file')

    parser.add_argument('--input', '-i', dest='infile', type=str,
                        help='file with chr pos to annotate per line')

    return parser.parse_args()


def parse_gtf(gtf_file):
    """
    Parse gtf file and sort for efficient queries for millions of chr/pos
    To make efficient searches, store one annotation for each gene with start/end coordinates
    input: gtf file
    Indexes of the output dictionary are chromosomes, entries are (start, end, gene_name)
    @return: dictionary of lists.
    """

    genes_indexed_chr = defaultdict(dict)

    with open(gtf_file, 'r') as f:
        for line in f.readlines():

            #parse columns
            columns = line.strip().split('\t')

            chrom = columns[0]
            annot_type = columns[2]
            start = int(columns[3])
            end = int(columns[4])
            attributes = columns[8]

            # Extract gene_name from attribute column
            gene_name = ""
            for attr in attributes.split(';'):
                if attr.strip().startswith('gene_name'):
                    gene_name = attr.split('"')[1] #gene name between quotes
                    break

            #skip introns, missing gene names, and undefined chromosomes
            if (annot_type != 'exon') or (gene_name == ""):
                continue

            if gene_name not in genes_indexed_chr[chrom]:
                #add gene if not in chr entry
                genes_indexed_chr[chrom][gene_name] = [start, end]

            else:
                #store only start (min) and end (max) coord of each gene
                #check and update lower and upper bounds of gene coord range for each exon
                genes_indexed_chr[chrom][gene_name][0] = min(genes_indexed_chr[chrom][gene_name][0], start)
                genes_indexed_chr[chrom][gene_name][1] = max(genes_indexed_chr[chrom][gene_name][1], end)


    #collapse dict of dicts into dict of lists; sort genes by start position
    sorted_collapsed = {}
    for chrom, genes in genes_indexed_chr.items():
        sorted_collapsed[chrom] = sorted(
            [(start, end, gene) for gene, (start, end) in genes.items()]
        )

    return sorted_collapsed


def find_overlap(genes, pos):
    """
    Binary search to efficiently find gene annotations in chrom for input position
    input: genes is a list of (start, end, gene_name) chrom entries sorted by start
    pos is the position
    @return: all genes that overlap the position
    """
    
    #keep track of points of left and right genes to search between
    left = 0
    right = len(genes) - 1
    
    results = []
    
    #loop until searched whole list (left and right points have crossed)
    while left <= right:
        
        mid = (left + right) // 2 #midpoint
        start, end, name = genes[mid]
        
        if start <= pos <= end:
            #if position is within first and last coord of midpoint gene 
            
            results.append(name)
            
            # Scan adjacent genes to catch overlapping with input position
            i = mid - 1
            while i >= 0 and genes[i][0] <= pos:
                if genes[i][1] >= pos:
                    results.append(genes[i][2])
                i -= 1
                
            i = mid + 1
            while i < len(genes) and genes[i][0] <= pos:
                if genes[i][1] >= pos:
                    results.append(genes[i][2])
                i += 1
            break

        elif pos < start:
            #if position is less than midpoint coord, search left half list
            right = mid - 1
            
        else:
            #if position is greater than midpoint coord, search right half list
            left = mid + 1
            
    return results


def annotate_positions(input_file, parsed_gtf, output_file):
    """
    Parse input file of chr pos to annotate
    Get genes overlapping input postion and write output file with annotation
    """
    
    missing_chr = [] #keep track of missing annotations

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:

        for line in infile.readlines():
            chrom, pos = line.strip().split()

            if chrom in parsed_gtf:
                #check if chromosome is in annotation
                #then search parsed gtf for gene overlap
                genes = find_overlap(parsed_gtf[chrom], int(pos))

                if genes != []:
                    outfile.write(f"{chrom}\t{pos}\t{','.join(set(genes))}\n")
                else:
                    #write . if no genes overlapping position
                    outfile.write(f"{chrom}\t{pos}\t.\n")
            else:
                if chrom not in missing_chr:
                    missing_chr.append(chrom)
                    print(f"Warning: {chrom} is not in annotation gtf.")
                    outfile.write(f"{chrom}\t{pos}\t.\n")


def main():
    print("Important Note: Make sure input coordinates and gtf are in the same genome build.")
    
    input_to_annotate  = get_cli_args().infile
    input_gtf = get_cli_args().gtf
    
    output_annotated = f"{'/'.join(input_to_annotate.split('/')[:-1])}/ANNOTATED_{input_to_annotate.split('/')[-1]}"

    parsed_gtf = parse_gtf(input_gtf)
    annotate_positions(input_to_annotate, parsed_gtf, output_annotated)
    
    print(f"Output annotated file was written to {output_annotated}\n")


if __name__ == '__main__':
    main()
