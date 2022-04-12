# Input: summary_table

# Output
# df1: dataframe with counts per species and gene
# df2: dataframe with labels present in each gene

import os
import numpy as np
import pandas as pd

gene_name = 'AYG1'
input_path = 'output_create_dict/'
result = os.listdir(input_path)

# open all labels file
summary = open(input_path + 'DHN_summary_table.txt').readlines()

# Get all unique species names
unique_names = []

for line in summary:
    if '~jgi~' in line:
        unique_names.append(line.split('|')[0])

# Remove duplicate species names from unique_names
unique_names = set(unique_names)

# Make matrices
column_names1 = ['ABR2', 'AYG1', 'PKS1', 'SCD1', 'RDT1']

matrix1 = np.zeros((len(unique_names),5))
matrix2 = np.zeros((len(unique_names),5))
df1 = pd.DataFrame(matrix1, columns=column_names1, index=unique_names)
df2 = pd.DataFrame(matrix2, columns=column_names1, index=unique_names)

# Add labels to df1
for line in summary:
    current_species = line.split('|')[0]
    for part_of_line in line.split('|')[1:]:
        gene = part_of_line.split(',')[0]
        label = part_of_line.split(',')[4]
        if 'jgi' in label:
            identifier = str(label.split('~')[3])
        df1[gene][current_species] += 1
        previous_info = str(df2[gene][current_species])
        if previous_info == str(0.0):
            df2[gene][current_species] = identifier
        else:
            new_info = str(previous_info) + ',' + identifier
            df2[gene][current_species] = new_info

df1.to_csv('gene_occurrence.csv')

# Uncomment below to get the latex format
# print(df1.to_latex(index=True))
# print(df2.to_latex(index=True))

