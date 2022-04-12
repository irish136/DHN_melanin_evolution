import random

jgi_taxonomy = open('JGI_taxonomy_species_class_order_family_genus.txt').readlines()
species_file = open('840_species_names.txt').readlines()

def create_annotation_file(taxonomy):
    if taxonomy == 'class':
        index = 1
    elif taxonomy == 'order':
        index = 2
    elif taxonomy == 'family':
        index = 3
    elif taxonomy == 'genus':
        index = 4
    else:
        print(taxonomy + ' cannot be processed, try "class", "order", "family" or "genus"')
        exit()

    rang = []
    dict_rang_color = dict()

    for line in jgi_taxonomy:
        rang.append(line.split(',')[index])

    rang = list(set(rang))

    for fungal_class in rang:
        r = lambda: random.randint(0, 255)
        hex_code = '#%02X%02X%02X' % (r(), r(), r())
        dict_rang_color[fungal_class.strip()] = hex_code

    legend_shapes_string = 'LEGEND_SHAPES,'
    legend_labels_string = 'LEGEND_LABELS,'
    legend_colors_string = 'LEGEND_COLORS,'

    for key in dict_rang_color.keys():
        legend_shapes_string += '1,'
        legend_labels_string += key + ','
        legend_colors_string += dict_rang_color[key] + ','

    # remove last ','
    legend_shapes_string = legend_shapes_string[:-1]
    legend_colors_string = legend_colors_string[:-1]
    legend_labels_string = legend_labels_string[:-1]


    f = open("species_tree_itol_annotation_" + taxonomy + ".txt", 'w+')
    f.write("DATASET_COLORSTRIP\n")
    f.write("SEPARATOR COMMA\n")
    f.write("DATASET_LABEL," + taxonomy + "\n")
    f.write("COLOR,#ff0000\n")
    f.write('LEGEND_TITLE,' + taxonomy + '\n')
    f.write(legend_shapes_string + '\n')
    f.write(legend_colors_string + '\n')
    f.write(legend_labels_string + '\n')
    f.write("DATA\n")

    for species in species_file:
        species = species.strip()
        for line in jgi_taxonomy:
            if line.split(',')[0] == species:
                species_rang = line.split(',')[index]
                color = dict_rang_color[species_rang.strip()]
                f.write('CONTAINS==' + species + ',' + color + '\n')

create_annotation_file('class')
