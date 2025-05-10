#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:01:08 2025

@author: Jessica Kelly

usage: python task3_ensemble.py [rsID_1],[rsID_2]
purpose: report Ensembl annotations for input list of variants
"""

import requests, sys
import argparse
import json
import pandas as pd


def get_cli_args():
    """
    Get the command line options using argparse
    @return: Instance of argparse arguments
    """

    parser = argparse.ArgumentParser(description="Give list of var ids")
    parser.add_argument('var_list', help="list of variants withought spaces (ex: rs123,rs456)")
    parser.add_argument('-o', '--out_excel', dest='out_excel',
                        type=str, default=False,
                        help="optional output filepath to excel (default: False)")

    return parser.parse_args()


def bad_request(r):
    """" handle bad API request """
    r.raise_for_status()
    sys.exit()


def ensembl_request_var_info(var_ids):
    """
    request Ensembl API variant info from list of ids
    @return: json formatted string of variant info
    """

    # format input list of ids for request string
    format_input = '","'.join(var_ids.replace(' ', '').split(','))
 
    server = "https://rest.ensembl.org"
    ext = "/vep/human/id"
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    r = requests.post(server+ext, headers=headers, data=str('{ "ids" : ["' + format_input + '"] }'))

    if not r.ok:
      bad_request(r)

    return r.json()

    
def main():
    """ main method to get ensembl annotations"""

    input_var_ids = get_cli_args().var_list
    info = ensembl_request_var_info(input_var_ids)

    print(json.dumps(info, indent=2))
    
    output = get_cli_args().out_excel
    if output:
            df = pd.json_normalize(info)
            df.to_excel(output)
            print(f"Ouput Excel written to {output}")


if __name__ == '__main__':
    main()
