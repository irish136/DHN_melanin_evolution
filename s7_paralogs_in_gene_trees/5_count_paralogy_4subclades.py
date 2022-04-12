# Input folder:
# 1: files containing the labels of a subclade, make sure that these files end with "subclade_labels.txt"
# 2: file containing all labels of the gene tree, make sure that these files end with "completetree_labels_adjusted.txt"
# For all input files: make sure that no spaces are present (use underscores instead of spaces)

# Output: latex table with how often 2, 3 or 4 paralogs are present in subclade combinations.

# Warning: this script is only for gene trees with 4 subclades!

# Import packages
import os
import itertools
import numpy as np
import pandas as pd

# Variables
gene = 'PKS1'
input_path = 'input_connections/' + gene + '/'
suffix_subclade = "subclade_labels.txt"
suffix_whole_tree = "completetree_labels_adjusted.txt"
result = os.listdir(input_path)

# Get difference of two lists
def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

# Get all combination of subclade names
def get_combinations():
    for L in range(1, len(subclade_names)+1):
        for subset in itertools.combinations(subclade_names, L):
            combination = ''
            for abbrev in list(subset):
                combination += abbrev + '_'
            # save combination in list of all row_names, remove last '_'
            combination = combination[:-1]
            row_names.append(combination)


# Create lists per subclade
def create_list_per_subclade():
    for subclade_file in subclade_files:
        subclade_name = subclade_file.split('_')[1]
        subclade = open(input_path + subclade_file).readlines()
        for line in subclade:
            if line.split('|')[1] == 'jgi':
                if subclade_name in dict:
                    # append the species to the existing key
                    dict[subclade_name].append(line.split('|')[2])
                else:
                    # create a new key
                    temp_list = []
                    temp_list.append(line.split('|')[2])
                    dict[subclade_name] = temp_list

def update_df(count, current_combination):
    if count == 2:
        df['2_paralogs'][current_combination] += 1
    elif count == 3:
        df['3_paralogs'][current_combination] += 1
    elif count == 4:
        df['4_paralogs'][current_combination] += 1

# Loop over each combination
def get_counts_per_paralog():
    for L in range(1, len(subclade_names)+1):
        for subset in itertools.combinations(subclade_names, L):
            current_combination = ''
            for abbrev in list(subset):
                current_combination += abbrev + '_'
            # save combination in list of all row_names, remove last '_'
            # this is needed for indexing the right row of the dataframe
            current_combination = current_combination[:-1]

            # Create a list with all subclades of current combination
            subset_list = []
            for subclade in subset:
                subset_list.append(subclade)

            # get subclade names not present in this specific subset
            non_subset_list = Diff(subclade_names, subset_list)

            # loop over species
            for species in unique_names:
                if len(subset_list) == 1:
                    # check if species is present in current subclade
                    # it's not needed to check if species is not present in other subclades, since this block
                    # checks for recent duplication events.
                    if species in dict[subset_list[0]]:
                        # check how often species is present in current subclade and add information to df
                        if dict[subset_list[0]].count(species) != 1:
                            # count how often species is present
                            count = dict[subset_list[0]].count(species)
                            # add info to df
                            update_df(count, current_combination)

                # check cases that species is present in 2 subclades
                elif len(subset_list) == 2:
                    # check if species is only present in current 2 subclades
                    if species in dict[subset_list[0]] and \
                            species in dict[subset_list[1]] and \
                            species not in dict[non_subset_list[0]] and \
                            species not in dict[non_subset_list[1]]:
                        # count how often species is present
                        count = dict[subset_list[0]].count(species) + dict[subset_list[1]].count(species)
                        # add info to df
                        update_df(count, current_combination)

                # check cases that species is present in 3 subclades
                elif len(subset_list) == 3:
                    # check if species is only present in current 3 subclades
                    if species in dict[subset_list[0]] and \
                            species in dict[subset_list[1]] and \
                            species in dict[subset_list[2]] and \
                            species not in dict[non_subset_list[0]]:
                        # count how often species is present
                        count = dict[subset_list[0]].count(species) + dict[subset_list[1]].count(species) + dict[subset_list[2]].count(species)
                        # add info to df
                        update_df(count, current_combination)

                # Check cases that species is present in 4 subclades
                elif len(subset_list) == 4:
                    # check if species is present in all 4 subclades
                    if species in dict[subset_list[0]] and \
                            species in dict[subset_list[1]] and \
                            species in dict[subset_list[2]] and \
                            species in dict[subset_list[3]]:
                        # count how often species is present (this should be 4)
                        count = dict[subset_list[0]].count(species) + dict[subset_list[1]].count(species) + dict[subset_list[2]].count(species) + dict[subset_list[3]].count(species)
                        # add info to df
                        update_df(count, current_combination)

# Main
# Open relevant data and put info in lists
subclade_files = []
subclade_names = []
all_labels_file = []
row_names = []
column_names = ['2_paralogs', '3_paralogs', '4_paralogs']

for i in result:
    if suffix_subclade in i:
        subclade_files.append(i)
        subclade_names.append(i.split('_')[1])
    elif suffix_whole_tree:
        all_labels_file.append(i)

# get all combinations and save in row_names
get_combinations()

# Make matrix
matrix = np.zeros((len(row_names),3))
df = pd.DataFrame(matrix, columns=column_names, index=row_names)

# Open all_labels_file
for file in all_labels_file:
    all_labels = open(input_path + file).readlines()

# Get all unique species names
unique_names = []

for label in all_labels:
    if label.split('|')[1] == 'jgi':
        unique_names.append(label.split('|')[2])

# Remove duplicate species names from unique_names
unique_names = set(unique_names)

# Update dictionary
dict = dict()
create_list_per_subclade()

# Get counts
get_counts_per_paralog()

# Get latex format
print(df.to_latex(index=True))