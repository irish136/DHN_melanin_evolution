paralogs = ["pks1_4thn_1", "pks1_4thn_2", "pks1_athn_1", "pks1_athn_2", "pks1_ywa1", "ayg1_1", "ayg1_2", "ayg1_3", "ayg1_cladeA", "ayg1_outgroup", "ayg1_yg1", "scd1_arp1", "scd1_cladeA", "scd1_cladeB", "scd1_cladeC", "scd1_outgroup", "rdt1_3hnr", "rdt1_4hnr_1", "rdt1_4hnr_2", "rdt1_4hnr_3", "rdt1_4hnr_4", "rdt1_arp2", "rdt1_cladeA", "rdt1_cladeB", "rdt1_outgroup", "rdt1_remaining", "abr2_abr1_1", "abr2_abr1_2", "abr2_abr1_3", "abr2_abr2_1", "abr2_abr2_2", "abr2_cladeA", "abr2_cladeB"]
# paralogs = ["pks1_4thn_1", "pks1_4thn_2"]

number_X = '4'

input_path = 'output_annotation_species_tree_figure/original_annotation/'
output_path = 'output_annotation_species_tree_figure/in_blocks/'

for paralog in paralogs:
    annotation_file = open(input_path + paralog + '_annotation_file' + number_X + '.txt').readlines()

    counter = 0
    for line in annotation_file:
        counter += 1

    if counter > 7:
        f = open(output_path + 'in_blocks_' + paralog + '_annotation_file' + number_X + '.txt', 'w+')

        f.write('DATASET_DOMAINS' + '\n' +
                'SEPARATOR COMMA' + '\n' +
                'DATASET_LABEL,' + paralog + '_annotation_file_' + number_X + '\n' +
                'COLOR,#ff0000' + '\n' +
                'WIDTH,150' + '\n' +
                'HEIGHT_FACTOR,2' + '\n' +
                'DATA' + '\n')

        # read annotation lines of file
        for line in annotation_file[7:]:
            species = line.split(',')[0]
            gene_info_list = []
            for gene_info in line.split(',')[2:]:
                gene_info_list.append(gene_info.strip())

            shape_list = []
            start_list = []
            end_list = []
            color_list = []
            name_list = []

            new_start_list = []
            new_end_list = []

            for gene in gene_info_list:
                shape_list.append(gene.split('|')[0])
                start_list.append(gene.split('|')[1])
                end_list.append(gene.split('|')[2])
                color_list.append(gene.split('|')[3])
                name_list.append(gene.split('|')[4])

            number_of_genes = len(name_list)

            for number in range(100, number_of_genes*300, 300):
                new_start_list.append(number)

            for number in range(300, number_of_genes*300+1, 300):
                new_end_list.append(number)

            some_length = new_end_list[-1] + 100

            output_line = species
            temp_string = ''

            for i in range(0, number_of_genes):
                temp_string += shape_list[i] + '|' + str(new_start_list[i]) + '|' + str(new_end_list[i]) + '|' + color_list[i] + '|' + name_list[i] + ','

            temp_string = temp_string[:-1]
            output_line += ',' + str(some_length) + ',' + temp_string
            f.write(output_line + '\n')