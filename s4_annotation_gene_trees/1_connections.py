# Input folder:
# 1: files containing the labels of a subclade, make sure that these files end with "subclade_labels.txt"
# 2: file containing all labels of the gene tree, make sure that these files end with "completetree_labels_adjusted.txt"
# For all input files: make sure that no spaces are present (use underscores instead of spaces)

# Output: at least three annotation files
# 1: annotation file with all connections
# 2: annotation file with connections between each subclade
# 3: annotation file with the connections per clade.

import os
from itertools import combinations

# Variables, change manually if needed
gene_name = 'ABR2'
input_path = "input_connections/" + gene_name + '/'
output_path = 'output_connections/' + gene_name + '/'
suffix_subclade = "subclade_labels.txt"
suffix_whole_tree = "completetree_labels_adjusted.txt"
input_files = os.listdir(input_path)
output_files = os.listdir(output_path)

# Create color dict
# Create dictionary with colours
color_dict = {}
color_dict['EUROTIO'] = '#ce7e00'
color_dict['DOTHIDEO'] = '#8fce00'
color_dict['LECANORO'] = '#2986cc'
color_dict['LEOTIO'] = '#6a329f'
color_dict['SORDARIO'] = '#6dbbcc'
color_dict['PEZIZO'] = '#f44336'
color_dict['XYLONO'] = '#990000'

# Functions
def rSubset(arr, r):
    return list(combinations(arr, r))

def get_species_names(all_labels_file):
    species_list = []
    for label in all_labels_file:
        if 'jgi' in label:
            species_list.append(label.split('|')[2])
    # keep only one copy if species occurs more than once
    species_list = set(species_list)
    return species_list

def get_all_connections(all_labels_file, species_list, gene_name, color_dict):
    list_labels_for_connections = []
    for species in species_list:
        labels_of_species = []
        for label in all_labels_file:
            if 'jgi' in label:
                current_species = label.split('|')[2]
            else:
                current_species = 'empty'
            if species == current_species:
                labels_of_species.append(label.strip())
                if len(labels_of_species) != 1 and labels_of_species != []:
                    list_labels_for_connections.append(labels_of_species)

    list_all_combinations = []

    for same_species_list in list_labels_for_connections:
        temp_list = rSubset(same_species_list, 2)
        list_all_combinations.append(temp_list)

    f = open(output_path + gene_name + "_itol_templ_all_connections.txt", 'w+')
    f.write("DATASET_CONNECTION\n")
    f.write("SEPARATOR COMMA\n")
    f.write("DATASET_LABEL,all_connections\n")
    f.write("COLOR,#000000\n")
    f.write("DRAW_ARROWS,0\n")
    f.write("MAXIMUM_LINE_WIDTH,3\n")
    f.write("DATA\n")

    for labels_of_species in list_all_combinations:
        for duo in labels_of_species:
            if duo[0].split('|')[0] != 'CHARACTERIZED':
                color = color_dict[duo[0].split('|')[0]]
                f.write(duo[0] + ',' + duo[1] + ',1,' + color + ',normal\n')

def get_connections_within_subclades(subclade_files, species_list, gene_name, color_dict):
    f = open(output_path + gene_name + "_itol_templ_connections_within_subclades.txt", 'w+')
    f.write("DATASET_CONNECTION\n")
    f.write("SEPARATOR COMMA\n")
    f.write("DATASET_LABEL,within_subclades_connections\n")
    f.write("COLOR,#000000\n")
    f.write("DRAW_ARROWS,0\n")
    f.write("MAXIMUM_LINE_WIDTH,3\n")
    f.write("DATA\n")
    for subclade_file in subclade_files:
        labels_file = open(input_path + subclade_file).readlines()
        list_labels_for_connections = []
        for species in species_list:
            labels_of_species = []
            for label in labels_file:
                if 'jgi' in label:
                    current_species = label.split('|')[2]
                else:
                    current_species = 'empty'
                if species == current_species:
                    labels_of_species.append(label.strip())
                    if len(labels_of_species) != 1 and labels_of_species != []:
                        list_labels_for_connections.append(labels_of_species)

        list_all_combinations = []

        for same_species_list in list_labels_for_connections:
            temp_list = rSubset(same_species_list, 2)
            list_all_combinations.append(temp_list)

        for labels_of_species in list_all_combinations:
            for duo in labels_of_species:
                if duo[0].split('|')[0] != 'CHARACTERIZED':
                    color = color_dict[duo[0].split('|')[0]]
                    f.write(duo[0] + ',' + duo[1] + ',1,' + color + ',normal\n')

def get_connections_per_class(all_connections_file, gene_name, output_path):
    connections_file = open(output_path + all_connections_file, 'r')
    connections = connections_file.readlines()[7:]

    classes = []

    for line in connections:
        if line.split('|')[0] not in classes:
            classes.append(line.split('|')[0])

    for fungal_class in classes:
        class_string = str(fungal_class)
        globals()[fungal_class] = open(output_path + gene_name + '_itol_templ_' + class_string + '_connections.txt', 'w')
        globals()[fungal_class].write("DATASET_CONNECTION\n")
        globals()[fungal_class].write("SEPARATOR COMMA\n")
        globals()[fungal_class].write("DATASET_LABEL,connections " + class_string + " same species\n")
        globals()[fungal_class].write("COLOR,#000000\n")
        globals()[fungal_class].write("DRAW_ARROWS,0\n")
        globals()[fungal_class].write("MAXIMUM_LINE_WIDTH,1\n")
        globals()[fungal_class].write("DATA\n")

    for line in connections:
        class_of_line = str(line.split('|')[0])
        globals()[class_of_line].write(line)

# Main
# Put relevant filenames in lists
subclade_files = []
subclade_names = []
all_labels_file = []

for i in input_files:
    if suffix_subclade in i:
        subclade_files.append(i)
        subclade_names.append(i.split('_')[1])
    elif suffix_whole_tree in i:
        all_labels_file.append(i)

# open file containing all labels
all_labels_file = open(input_path + all_labels_file[0]).readlines()

# Get all unique species names
species_list = get_species_names(all_labels_file)

# Get all connections
get_all_connections(all_labels_file, species_list, gene_name, color_dict)

# Get connections within subclade
get_connections_within_subclades(subclade_files, species_list, gene_name, color_dict)

# Get connections per class
for i in output_files:
    if "all_connections.txt" in i:
        get_connections_per_class(i, gene_name, output_path)