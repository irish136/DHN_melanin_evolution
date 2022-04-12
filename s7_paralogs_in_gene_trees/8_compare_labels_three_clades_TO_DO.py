# This code takes two files with labels as input
# Produces a list with different species and same species

import os
import itertools
import numpy as np
import pandas as pd

input_path = 'input_compare_labels/'
result = os.listdir(input_path)

label_files = []

for i in result:
    if ".txt" in i:
        label_files.append(i)

file_1 = open(input_path + label_files[0])
file_2 = open(input_path + label_files[1])
file_3 = open(input_path + label_files[2])


species_file1 = []
species_file2 = []
species_file3 = []

# Get unique species names of file 1
for label in file_1:
    if 'jgi' in label:
        species_file1.append(label.split('|')[2])
species_file1 = set(species_file1) # keep one species name if there are copies

# Get unique species names of file 2
for label in file_2:
    if 'jgi' in label:
        species_file2.append(label.split('|')[2])
species_file2 = set(species_file2) # keep one species name if there are copies

# Get unique species names of file 3
for label in file_3:
    if 'jgi' in label:
        species_file3.append(label.split('|')[2])
species_file3 = set(species_file3) # keep one species name if there are copies

# Number of species present in file 1 but not in file 2 and 3
only_file1 = species_file1 - species_file2 - species_file3

# Number of species present in file 2 but not in file 1 and 3
only_file2 = species_file2 - species_file1 - species_file3

# Number of species present in file 3 but not in file 1 and 2
only_file3 = species_file3 - species_file1 - species_file2

# Number of species present in both files
all_files = species_file1 & species_file2 & species_file3
#print(both_files)


print(label_files[0] + ',    # unique species: ', len(species_file1), ',  # species only in file 1: ', len(only_file1))
print(label_files[1] + ',    # unique species: ', len(species_file2), ',  # species only in file 2: ', len(only_file2))
print(label_files[2] + ',    # unique species: ', len(species_file3), ',  # species only in file 3: ', len(only_file3))
print('species in all files: ', all_files)
print('# species in all files: ', len(all_files))



