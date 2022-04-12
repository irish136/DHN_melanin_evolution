# TO DO: DESCRIPTION


# open relevant fiiles
summary_table = open('output_create_dict/DHN_summary_table.txt').readlines()

input_path = 'input_compare_labels/all_paralogs/'

output_path = 'output_annotation_species_tree_figure/original_annotation/'

def write_annotation_file(line, chosen_scaffold, annotation_number, exclusive_dict, f1, f2, f3, f4):
    gene_info_list = []

    current_species = line.split('|')[0]


    for gene_info in line.split('|')[1:]:
        if chosen_scaffold == gene_info.split(',')[1] and current_species not in exclusive_dict.keys():
            gene_info_list.append(gene_info.strip())
        elif chosen_scaffold == gene_info.split(',')[1] and chosen_scaffold not in exclusive_dict[current_species]:
                gene_info_list.append(gene_info.strip())

    if gene_info_list != []:
        genes = ['ABR2', 'AYG1', 'PKS1', 'RDT1', 'SCD1']
        colors = ['#f44336', '#f1c232', '#00ff00', '#0000ff', '#c90076']

        output_line = current_species
        temp_string = ''

        some_length = 0

        # if you want to show the ones that there are at least two at the same scaffold
        # un comment line below and index everything with one tap
        # if len(gene_info_list) >= 2:
        for gene_info in gene_info_list:
            gene = gene_info.split(',')[0]
            start = gene_info.split(',')[2]
            end = gene_info.split(',')[3]

            # check for length of scaffold
            if int(start) > int(end) and int(start) > some_length:
                some_length = int(start)
            elif int(end) > int(start) and int(end) > some_length:
                some_length = int(end)

            if int(end) < int(start):
                copy_start = start
                copy_end = end
                start = copy_end
                end = copy_start
                shape = 'TL'
            else:
                shape = 'TR'
            color_index = genes.index(gene)
            color = colors[color_index]

            temp_string += ',' + shape + '|' + start + '|' + end + '|' + color + '|' + gene

            if output_line == current_species:
                output_line += ',' + str(some_length) + temp_string
            else:
                output_line += temp_string

        # output_line = output_line[:-1]

        if annotation_number == 'one':
            f1.write(output_line + '\n')
        if annotation_number == 'two':
            f2.write(output_line + '\n')
        elif annotation_number == 'three':
            f3.write(output_line + '\n')
        elif annotation_number == 'four':
            f4.write(output_line + '\n')

exclusive_dict = dict()

paralog_files = ["pks1_4thn_1", "pks1_4thn_2", "pks1_athn_1", "pks1_athn_2", "pks1_ywa1", "ayg1_1", "ayg1_2", "ayg1_3", "ayg1_cladeA", "ayg1_outgroup", "ayg1_yg1", "scd1_arp1", "scd1_cladeA", "scd1_cladeB", "scd1_cladeC", "scd1_outgroup", "rdt1_3hnr", "rdt1_4hnr_1", "rdt1_4hnr_2", "rdt1_4hnr_3", "rdt1_4hnr_4", "rdt1_arp2", "rdt1_cladeA", "rdt1_cladeB", "rdt1_outgroup", "rdt1_remaining", "abr2_abr1_1", "abr2_abr1_2", "abr2_abr1_3", "abr2_abr2_1", "abr2_abr2_2", "abr2_cladeA", "abr2_cladeB"]

# paralog_files = ["pks1_4thn_1", "pks1_4thn_2"]


# check labels per paralog
for file in paralog_files:
    species_of_paralog = []
    chosen_paralog = str(file)
    chosen_scaffolds_of_gene = 'empty'
    dict_of_paralog = dict()
    paralog_file = open(input_path + file + '.txt').readlines()

    f1 = open(output_path + chosen_paralog + '_annotation_file1.txt', 'w+')
    f2 = open(output_path + chosen_paralog + '_annotation_file2.txt', 'w+')
    f3 = open(output_path + chosen_paralog + '_annotation_file3.txt', 'w+')
    f4 = open(output_path + chosen_paralog + '_annotation_file4.txt', 'w+')

    data_set_domains_template = 'DATASET_DOMAINS' + '\n' + 'SEPARATOR COMMA' + '\n' + 'DATASET_LABEL,chosen_scaffold' + '\n' + 'COLOR,#ff0000' + '\n' + 'WIDTH,150' + '\n' + 'HEIGHT_FACTOR,2' + '\n' + 'DATA' + '\n'

    f1.write(data_set_domains_template)
    f2.write(data_set_domains_template)
    f3.write(data_set_domains_template)
    f4.write(data_set_domains_template)

    for line in paralog_file:
        if 'CHARACTERIZED' not in line:
            species = line.split('|')[2]
            id = line.split('|')[3]
            if species in dict_of_paralog:
                dict_of_paralog[species].append(id)
            else:
                dict_of_paralog[species] = [id]

    # loop over species
    for line in summary_table:
        current_species = line.split('|')[0]

        chosen_scaffolds_of_gene = []
        if line.split('|')[0] in dict_of_paralog.keys():
            for gene_info in line.split('|')[1:]:
                if 'CHARACTERIZED' not in gene_info:
                    id_of_gene_info = gene_info.split('~')[3]

                    if len(dict_of_paralog[current_species]) >= 2:
                        for id in dict_of_paralog[current_species]:
                            if id == id_of_gene_info:
                                chosen_scaffolds_of_gene.append(gene_info.split(',')[1])
                    else:
                        if dict_of_paralog[current_species][0] == id_of_gene_info:
                            chosen_scaffolds_of_gene.append(gene_info.split(',')[1])

        chosen_scaffolds_of_gene = list(set(chosen_scaffolds_of_gene))

        if len(chosen_scaffolds_of_gene) == 4:
            write_annotation_file(line, chosen_scaffolds_of_gene[0], 'one', exclusive_dict, f1, f2, f3, f4)
            write_annotation_file(line, chosen_scaffolds_of_gene[1], 'two', exclusive_dict, f1, f2, f3, f4)
            write_annotation_file(line, chosen_scaffolds_of_gene[2], 'three', exclusive_dict, f1, f2, f3, f4)
            write_annotation_file(line, chosen_scaffolds_of_gene[3], 'four', exclusive_dict, f1, f2, f3, f4)
        if len(chosen_scaffolds_of_gene) == 3:
            write_annotation_file(line, chosen_scaffolds_of_gene[0], 'one', exclusive_dict, f1, f2, f3, f4)
            write_annotation_file(line, chosen_scaffolds_of_gene[1], 'two', exclusive_dict, f1, f2, f3, f4)
            write_annotation_file(line, chosen_scaffolds_of_gene[2], 'three', exclusive_dict, f1, f2, f3, f4)
        if len(chosen_scaffolds_of_gene) == 2:
            write_annotation_file(line, chosen_scaffolds_of_gene[0], 'one', exclusive_dict, f1, f2, f3, f4)
            write_annotation_file(line, chosen_scaffolds_of_gene[1], 'two', exclusive_dict, f1, f2, f3, f4)
        if len(chosen_scaffolds_of_gene) == 1:
            write_annotation_file(line, chosen_scaffolds_of_gene[0], 'one', exclusive_dict, f1, f2, f3, f4)


        if chosen_scaffolds_of_gene != 'empty':
            for scaffold in chosen_scaffolds_of_gene:
                if current_species in exclusive_dict:
                    exclusive_dict[current_species].append(scaffold)
                else:
                    exclusive_dict[current_species] = [scaffold]


