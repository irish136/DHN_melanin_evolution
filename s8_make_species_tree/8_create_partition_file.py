import os
import gzip

#IQtree_files_path = 'output_iqtree_v3/'
trimal_files_path = 'output_trimal_per_gene_v3/'
output_path = 'output_partition_files_v3/'

new_fasta = open(output_path + 'new_fasta.fasta', 'w+')

species_file = open('840_species_names.txt').readlines()

# partition_file = open(output_path + 'partition_file.nex', 'w+')
# partition_file.write('#nexus\n')
# partition_file.write('begin sets;\n')

data = os.listdir(trimal_files_path)
gene_names = []
big_fasta_dict = dict()

for species in species_file:
    big_fasta_dict[species.strip()] = ''

charpartition_mine = '  charpartition mine = '

for i in data:
    if ".fasta.gz" in i:
        gene_names.append(i.split('.')[0].split('_')[1])

start = 1

counter = 0

for gene_name in gene_names:
    print(gene_name)
    print(counter)
    counter += 1
    with gzip.open(trimal_files_path + 'trimal_' + gene_name + '.fasta.gz', 'rt') as trimal_of_gene:
        for line in trimal_of_gene:
            if line.startswith('>'):
                trimal_species = line.split('>')[1].strip()
            else:
                current_sequence = big_fasta_dict[trimal_species]
                new_sequence = current_sequence + line.strip()
                big_fasta_dict[trimal_species] = new_sequence
        # length_of_gene = len(big_fasta_dict[trimal_species])
        # end = length_of_gene
        # partition_file.write('  charset ' + gene_name + ' = ' + str(start) + '-' + str(end) + ';' + '\n')
        # start = end + 1

    # IQtree_output = open(IQtree_files_path + gene_name + '.iqtree')
    # for line in IQtree_output:
    #     if 'Best-fit model according to BIC:' in line:
    #         best_model_BIC = line.split(': ')[1]
    #         charpartition_mine += str(best_model_BIC.strip()) + ':' + gene_name + ', '

# # Remove the last ', ' of charpartition
# charpartition_mine = charpartition_mine[:-2]
#
# # Add ';' to charpartition
# charpartition_mine += ';'
#
# partition_file.write(charpartition_mine + '\n')
# partition_file.write('end;')

for species in species_file:
    species = species.strip()
    header = '>' + species
    sequence = big_fasta_dict[species]
    new_fasta.write(header + '\n')
    new_fasta.write(sequence + '\n')
