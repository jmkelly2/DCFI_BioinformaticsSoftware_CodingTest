#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:01:08 2025

@author: kellyjes
"""

import requests, sys
import pandas as pd


#input_var_ids = sys.argv[1]
input_var_ids = "rs56116432, COSM476"
format_input = '","'.join(input_var_ids.replace(' ', '').split(','))

 
server = "https://rest.ensembl.org"
ext = "/vep/human/id"
headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
r = requests.post(server+ext, headers=headers, data=str('{ "ids" : ["' + format_input + '"] }'))
 
if not r.ok:
  r.raise_for_status()
  sys.exit()
 
decoded = r.json()
test= repr(decoded)
df = pd.DataFrame(decoded)

print(test)
