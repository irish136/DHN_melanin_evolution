# This code takes all DHN labels as input
# Output: it counts how often each paralog combination occurs, i.e. ~abr2_abr1_1~abr2_abr2_1: 1

import os
from collections import Counter

# Get data names and positions
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

# Count paralog combinations
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

# Get counts
res = Counter(dict1.values())

# Save in output
output_file = open('occurence_counts.txt', 'w')

for element in res:
    print(res[element])
    output_file.write(element + ': ' + str(res[element]) + '\n')
