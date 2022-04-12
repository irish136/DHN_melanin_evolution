# Input folder:
# 1: file containing the JGI taxonomy (check if path described in this taxonomy file corresponds to the path
# of the downloaded JGI data).

# 2: file containing all labels of the gene tree, i.e. PKS1_all_labels.txt
# For all input files: make sure that no spaces are present (use underscores instead of spaces)

# Output: at least three annotation files
# 1: annotation file with all connections
# 2: annotation file with connections between each subclade
# 3: annotation file with the connections per clade.

# Import packages
import gzip

# Variables
gene = 'PKS1'
input_path = 'input_retrieve_positions/'
output_path = 'output_retrieve_positions/'
suffix_all_labels = '_all_labels.txt'
taxonomy_name = 'JGI_taxonomy.tsv'

# Open tsv file with jgi taxonomy info
taxonomy = open(input_path + taxonomy_name, 'r').readlines()

# Open label file
labels = open(input_path + gene + suffix_all_labels, 'r').readlines()

# Create output file
f = open(output_path + gene + "_positions.txt", 'w+')

path = 'empty'
GFF_file = 'empty'

# Get positions for each label
for label in labels:
    start = 'empty'
    end = 'empty'

    # Get protein id
    if label.split('~')[1] == 'jgi':
        species_label = label.split('~')[2]
        protein_id_label1 = 'proteinId=' + str(label.split('~')[3]) + ';'
        protein_id_label2 = 'proteinId ' + str(label.split('~')[3]) + ';'
        protein_id_label3 = 'name "' + str(label.split('~')[4]).strip() + '"'

        # Open GFF file of this species
        for line in taxonomy:
            if species_label in line:
                path = line.split(',')[4]
                GFF_file = line.split(',')[6]

        GFF = gzip.open(path + '/' + GFF_file, 'rt').readlines()

        # Save positions and orientation in output file
        for line in GFF:
            if species_label in line and protein_id_label1 in line and line.split()[2] == 'gene':
                scaffold = line.split()[0]
                start = line.split()[3]
                end = line.split()[4]
                orientation = line.split()[6]
                f.write(scaffold + ',' + start + ',' + end + ',' + orientation + ',' + label)
            elif protein_id_label2 in line:
                scaffold = line.split()[0]
                orientation = line.split()[6]
                if 'start_codon' in line:
                    start = line.split()[3]
                if 'stop_codon' in line:
                    end = line.split()[4]
                if end != 'empty' and start != 'empty':
                    f.write(scaffold + ',' + start + ',' + end + ',' + orientation + ',' + label)
            elif protein_id_label3 in line:
                scaffold = line.split()[0]
                orientation = line.split()[6]
                if 'start_codon' in line:
                    start = line.split()[3]
                if 'stop_codon' in line:
                    end = line.split()[4]
                if end != 'empty' and start != 'empty':
                    f.write(scaffold + ',' + start + ',' + end + ',' + orientation + ',' + label)
