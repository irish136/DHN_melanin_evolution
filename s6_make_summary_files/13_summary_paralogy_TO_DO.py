import os
import numpy as np
import pandas as pd

input_path = 'input_compare_labels/all_paralogs/'
paralog_file_names = os.listdir(input_path)

all_labels = open('labels_all_dhn_trees.txt').readlines()

# create matrix
row_names = []
column_names = []

for paralog in paralog_file_names:
    column_names.append(paralog.split('.')[0])

for label in all_labels:
    if 'CHARACTERIZED' not in label:
        species = label.split('|')[2]
        if species not in row_names:
            row_names.append(species)

# Make matrix
matrix_for_ids = np.empty([len(row_names),len(column_names)], dtype=str)
df_with_ids = pd.DataFrame(matrix_for_ids, columns=column_names, index=row_names)
matrix_for_numbers = np.zeros((len(row_names),len(column_names)))
df_with_numbers = pd.DataFrame(matrix_for_numbers, columns=column_names, index=row_names)

counter = 0

for label in all_labels:
    counter += 1
    print(counter)
    if 'CHARACTERIZED' not in label:
        for file_name in paralog_file_names:
            file = open(input_path + file_name).readlines()
            for line in file:
                if label.strip() == line.strip():
                    species = line.split('|')[2]
                    paralog = file_name.split('.')[0]
                    id = line.split('|')[3]
                    previous_value = df_with_ids[paralog][species]
                    if previous_value == '':
                        df_with_ids[paralog][species] = id
                    else:
                        new_value = previous_value + ',' + id
                        df_with_ids[paralog][species] = new_value

                    df_with_numbers[paralog][species] += 1


df_with_ids.to_csv('table_species_vs_paralogs_identifiers.txt')
df_with_numbers.to_csv('table_species_vs_paralogs_counts.txt')
