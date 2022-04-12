# Input:
# 1: file containing all DHN labels
# 2: files containing position information of labels per gene

# Output:
# Summary file:
# Each species is on one line with its corresponding gene and position information

# Variables
input_path = 'input_create_dict/'
output_path = 'output_create_dict/'
all_positions_file = 'DHN_all_positions.txt'
output_file = 'DHN_summary_table.txt'

def create_dict(all_positions):
    dict_all = {}

    for line in all_positions:
        species = line.split('~')[2]
        dict_all.setdefault(species, [])
        dict_all[species].append(line.strip())

    f = open(output_path + output_file, 'w+')

    for key in dict_all:
        line = str(key)
        counter = 1
        for value in dict_all[key]:
            line += '|' + str(value)
            if counter == len(dict_all[key]):
                line += '\n'
            counter += 1
        f.write(line)
    return dict_all

# Main
all_positions = open(input_path + all_positions_file).readlines()

dict_all = create_dict(all_positions)