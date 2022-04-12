import os

# abspath to a folder as a string
import shutil

dir = os.getcwd()


# put species from own trees in list
all_labels = open('../labels_all_dhn_trees.txt').readlines()
all_species = []
for line in all_labels:
    if '|jgi|' in line:
        all_species.append(line.split('|')[2])

all_species = list(set(all_species))  # remove duplicates
#print(len(all_species))

all_species.append('DOTHIDEOMYCETES')
all_species.append('EUROTIOMYCETES')
all_species.append('LECANOROMYCETES')
all_species.append('LEOTIOMYCETES')
all_species.append('no_rank')
all_species.append('ORBILIOMYCETES')
all_species.append('PEZIZOMYCETES')
all_species.append('SORDARIOMYCETES')
all_species.append('XYLONOMYCETES')
# all_species.append('gffs')
# all_species.append('assemblies')


folders_to_remove = []

all_folders = []

for root, dirs, files in os.walk(dir):
    for name in dirs:
        all_folders.append(name)
        if name not in all_species:
            folders_to_remove.append(name)
            shutil.rmtree(os.path.join(root, name))

# print(all_folders)

folders_to_remove = list(set(folders_to_remove))
print(len(folders_to_remove))
