import gzip
import os

input_path = 'output_hmmsearch/'
output_path = 'hmmsearch_intersection/'
result = os.listdir(input_path)

long_list = open(output_path + 'all_presence_once_good.txt').readlines()
unique_long_list = list(set(long_list))

output_file = open(output_path + 'accurate_bigger_table1_925_930.txt', 'w+')

def count_genes(long_list, unique_long_list, threshold):
    intersection_result = []
    for gene in unique_long_list:
        if long_list.count(gene) >= threshold:
            intersection_result.append(gene.strip())
    return intersection_result



def count_species(file, gene_list, counter):
    with gzip.open(input_path + file, 'rt') as f:

        # genes_in_species is a list that contains the genes that are present in this species
        # incl duplicates
        genes_in_species = []

        for line in f:
            if not line.startswith('#'):
                gene_name = line.split('-')[1].strip()
                genes_in_species.append(gene_name.strip())

        genes_in_species_without_duplicates = list(set(genes_in_species))

        # check if all 928 genes are in this hmmsearch output file of this specific species
        result = all(elem in genes_in_species_without_duplicates for elem in gene_list)
        if result:
            counter += 1

        return counter


# Save filenames from hmmsearch output in files
files = []
for i in result:
    if i != 'predicted_genes_aa_Aspoch1.txt.gz' and i != 'predicted_genes_aa_Aspnom1.txt.gz' and i != 'predicted_genes_aa_Xylcur1.txt.gz' and i != 'predicted_genes_aa_Aspcal1.txt.gz':
        files.append(i)

for i in range(925, 930, 1):
    counter = 0
    genes_above_threshold = count_genes(long_list, unique_long_list, i)
    for file in files:
        counter = count_species(file, genes_above_threshold, counter)

    print(str(i) + ' ' + str(len(genes_above_threshold)) + '  ' + str(counter))
    output_file.write(str(i) + ' ' + str(len(genes_above_threshold)) + '  ' + str(counter) + '\n')
