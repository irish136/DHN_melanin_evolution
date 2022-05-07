# This code saves all genes that are present only once in each species, but
# at the same time present in all species
# Input: HMMsearch output
# Output 1: .txt file containing all genes that are present once in each species
# Output 2: .txt file containing all genes that are present once in each species and present in X/all species

# Import packages
import gzip
import os

# Get relevant directories
input_path = 'output_hmmsearch/'
output_path = 'hmmsearch_intersection/'
result = os.listdir(input_path)

# Variables
number_of_species = 938

def get_intersections(file):
    genes_present_once_in_species = []
    with gzip.open(input_path + file, 'rt') as f:

        # genes_in_species is a list that contains the genes that are present in this species
        # incl duplicates
        genes_in_species = []

        for line in f:
            if not line.startswith('#'): # skip commented lines
                gene_name = line.split('-')[1]
                genes_in_species.append(gene_name.strip())

        # Save genes that are only present once in genes_present_once_in_species
        for gene in genes_in_species:
            if genes_in_species.count(gene) == 1:
                genes_present_once_in_species.append(gene)
    return genes_present_once_in_species

# Get filenames from hmmsearch output
files = []
for i in result:
    # Four files need to be excluded
    if i != 'predicted_genes_aa_Aspoch1.txt.gz' and i != 'predicted_genes_aa_Aspnom1.txt.gz' and \
            i != 'predicted_genes_aa_Xylcur1.txt.gz' and i != 'predicted_genes_aa_Aspcal1.txt.gz':
        files.append(i)

all_presence_once = []

for file in files:
    # Save list with genes that are present once in one hmmsearch output file
    present_once_in_species = get_intersections(file)

    # Save these genes in file that is about all hmmsearch output: all_presence_once
    for gene in present_once_in_species:
        all_presence_once.append(gene)

# Check which genes are present in all species (but inside one species just once)
intersection_result = []

present_genes_list = list(set(all_presence_once)) # Remove duplicates

for gene in present_genes_list:
    if all_presence_once.count(gene) >= number_of_species:
        intersection_result.append(gene)

# Save intersection result
intersection_file = open(output_path + 'intersection_file.txt', 'w')
for gene in intersection_result:
    intersection_file.write(gene+ '\n')

# Save list with genes that occur once in each species, but from all species in one file
output_file = open(output_path + 'all_presence_once_good.txt', 'w')
for gene in all_presence_once:
    output_file.write(gene+ '\n')
