import gzip
import os

gff_path = 'gffs/original_gffs/'
g_fasta_path = 'output_bedtools/output_bedtools/'
hmmsearch_path = 'output_hmmsearch/'
output_path = 'output_fastas_per_gene_v3/'

gff_files = os.listdir(gff_path)
g_fasta_files = os.listdir(g_fasta_path)
hmmsearch_files = os.listdir(hmmsearch_path)

genes = open('1_5.txt').readlines()

species = open('840_species.txt').readlines()
species_list = []
for i in species:
    species_list.append(i.strip())


def create_fasta_per_gene(gene):
    counter = 0
    print('counter: ', counter)
    counter += 1
    output_file = open(output_path + gene + '.txt', 'w')

    for hmmsearch_file in hmmsearch_files:
        with gzip.open(hmmsearch_path + hmmsearch_file, 'rt') as hmmsearch_output:
            species = hmmsearch_file.split('_genes_aa_')[1].split('.txt')[0]
            if species in species_list:
            #print('species: ', species)
                for line in hmmsearch_output:
                    if not line.startswith('#'):
                        query_name = line.split('-')[1].strip()
                        if query_name == gene:
                            target_name = line.split('-')[0].strip()

                if 'mRNA_' in target_name:
                    gene_ID = target_name.split('RNA_')[1]
                elif 'mRNA' in target_name and 'mRNA_' not in target_name:
                    gene_ID = target_name.split('RNA')[1]
                else:
                    print('ERROR: OTHER TARGET NAME: ', target_name)
                    exit()

                gene_name = 'ID=gene_' + gene_ID + ';'

                for gff_file in gff_files:
                    if species in gff_file:
                        with gzip.open(gff_path + gff_file, 'rt') as gff_output:
                            for line in gff_output:
                                if gene_name in line:
                                    scaffold = line.split()[0]
                                    start = line.split()[3]
                                    end = line.split()[4]
                                    orientation = line.split()[6]

                            if int(end)<int(start):
                                new_end = start
                                new_start = end
                                start = new_start
                                end = new_end

                            start = str(int(start) - 1)

                            fasta_header = '>' + scaffold + ':' + start + '-' + end

                            for g_fasta_file in g_fasta_files:
                                if species in g_fasta_file:
                                    with gzip.open(g_fasta_path + g_fasta_file, 'rt') as g_fasta_output:
                                        g_fasta_output = g_fasta_output.readlines()
                                        for i in range(0, len(g_fasta_output)-1, 2):
                                            if g_fasta_output[i].strip() == fasta_header:
                                                output_file.write('>' + species.strip() + '\n')

                                                if orientation == '+':
                                                    output_file.write(g_fasta_output[i + 1].strip() + '\n')
                                                elif orientation == '-':
                                                    complement = ''
                                                    for nucleotide in g_fasta_output[i + 1]:
                                                        if nucleotide == 'A':
                                                            complement += 'T'
                                                        elif nucleotide == 'C':
                                                            complement += 'G'
                                                        elif nucleotide == 'T':
                                                            complement += 'A'
                                                        elif nucleotide == 'G':
                                                            complement += 'C'
                                                    reverse_complement = complement[::-1]
                                                    output_file.write(reverse_complement.strip() + '\n')
                                                else:
                                                    print('other orientation than "+" and "-"')

for gene in genes:
    create_fasta_per_gene(gene.strip())






