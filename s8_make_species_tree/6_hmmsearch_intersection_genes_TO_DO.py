import gzip
import os

# Input: one gff file
# Output: adjusted gff file

input_path = 'output_hmmsearch/'
output_path = 'hmmsearch_intersection/'
result = os.listdir(input_path)


def get_intersections(file):
    genes_present_once_in_species = []
    with gzip.open(input_path + file, 'rt') as f:

        # genes_in_species is a list that contains the genes that are present in this species
        # incl duplicates
        genes_in_species = []

        for line in f:
            if not line.startswith('#'):
                gene_name = line.split('-')[1]
                genes_in_species.append(gene_name.strip())

        # Save genes that are only present once in genes_present_once_in_species
        for gene in genes_in_species:
            if genes_in_species.count(gene) == 1:
                genes_present_once_in_species.append(gene)
    return genes_present_once_in_species

# Save filenames from hmmsearch output in files
files = []
for i in result:
    if i != 'predicted_genes_aa_Aspoch1.txt.gz' and i != 'predicted_genes_aa_Aspnom1.txt.gz' and i != 'predicted_genes_aa_Xylcur1.txt.gz' and i != 'predicted_genes_aa_Aspcal1.txt.gz':
        files.append(i)

# Use a counter to keep track of progress
counter = 0

all_presence_once = []

for file in files:
    print('file loop: ', counter)
    counter += 1
    # Save list with genes that are present once in one hmmsearch output file
    present_once_in_species = get_intersections(file)

    # Save these genes in file that is about all hmmsearch output: all_presence_once
    for gene in present_once_in_species:
        all_presence_once.append(gene)

# Check which genes are present in all species (but inside one species just once)
intersection_result = []

present_genes_list = list(set(all_presence_once))

for gene in present_genes_list:
    if all_presence_once.count(gene) >= 900: #should be 938
        intersection_result.append(gene)

# Save intersection result
intersection_file = open(output_path + 'intersection_file_3.txt', 'w')
for gene in intersection_result:
    intersection_file.write(gene+ '\n')

# Save list with genes that occur once in each species, but from all species in one file
test_output_file = open(output_path + 'all_presence_once_good.txt', 'w')
for gene in all_presence_once:
    test_output_file.write(gene+ '\n')