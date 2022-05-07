# This script removes the species folders (including assemblies and
# annotation) of species that are not present in the trees in order
# to save memory.
# Input: .txt file with all species names that need to be kept
# Output: extra folders are removed


# Improve libraries
import os
import shutil

# Get current working directory
dir = os.getcwd()

# Open species from own trees
all_labels = open('../labels_all_dhn_trees.txt').readlines()

all_species = []
folders_to_remove = []
all_folders = []

# Save species from own trees in list
for line in all_labels:
    if '|jgi|' in line:
        all_species.append(line.split('|')[2])
all_species = list(set(all_species))  # remove duplicates

# Classes of which species should be included
all_species.append('DOTHIDEOMYCETES')
all_species.append('EUROTIOMYCETES')
all_species.append('LECANOROMYCETES')
all_species.append('LEOTIOMYCETES')
all_species.append('no_rank')
all_species.append('ORBILIOMYCETES')
all_species.append('PEZIZOMYCETES')
all_species.append('SORDARIOMYCETES')
all_species.append('XYLONOMYCETES')

# Loop over downloaded JGI taxonomy folders and remove species that are not
# present in the tree
for root, dirs, files in os.walk(dir):
    for name in dirs:
        all_folders.append(name)
        if name not in all_species:
            folders_to_remove.append(name)
            shutil.rmtree(os.path.join(root, name))

# Check if right folders are selected
# folders_to_remove = list(set(folders_to_remove))
# print(len(folders_to_remove))
