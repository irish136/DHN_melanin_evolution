import os
from collections import Counter
import json
import itertools
import numpy as np
import pandas as pd

input_path = 'input_compare_labels/all_sub_subclades/'
result = os.listdir(input_path)

species_file = open('all_DHN_species.txt').readlines()

# Open relevant data and put info in lists
subclade_files = []
subclade_names = []

for i in result:
    if ".txt" in i:
        subclade_files.append(i)
        subclade_names.append(i.split('.')[0])
#
# # Get all combination of subclade names
# for L in range(1, len(subclade_names)+1):
#     for subset in itertools.combinations(subclade_names, L):
#         print(subset)

dict1 = dict()
counter = 0

for line in species_file:
    counter += 1
    species = line.strip()
    gene_presence = ''
    for subclade_name in subclade_names:
        file = open(input_path + subclade_name + '.txt').readlines()
        for line in file:
            if species in line:
                gene_presence += '~' + subclade_name
    dict1[species] = gene_presence
    print(counter)

res = Counter(dict1.values())
#print(res)

# test = Counter({'': 140, '_ayg1_1_ayg1_cladeA_pks1_4thn_1_rdt1_3hnr_rdt1_4hnr_1_scd1_all': 60})

new_file2 = open('occurence_counts.txt', 'w')

for element in res:
    print(res[element])
    new_file2.write(element + ': ' + str(res[element]) + '\n')
