# This script implements the orientation directly in the start and stop positions instead of using '-' and '+' symbols
# The input is the output of script 2_retrieve_positions.py.

# Import packages
import os

input_path = 'output_retrieve_positions/'
output_path = 'output_implement_orientation/'
result = os.listdir(input_path)

# Implement orientation

# Loop over output files from script 2_retrieve_positions.py
for i in result:
    if i.endswith('.txt'):
        file = open(input_path + i).readlines()
        gene_name = i.split('_')[0]

        f = open(output_path + gene_name + '_positions_incl_orientation.txt', 'w+')

        for line in file:
            first_position = line.split(',')[1]
            second_position = line.split(',')[2]
            if line.split(',')[3] == '-':

                if int(first_position) < int(second_position):
                    start = second_position
                    end = first_position
                else:
                    start = first_position
                    end = second_position

                f.write(gene_name + ',' + line.split(',')[0] + ',' + start + ',' +
                        end + ',' + line.split(',')[4])

            elif line.split(',')[3] == '+':

                if int(first_position) < int(second_position):
                    start = first_position
                    end = second_position
                else:
                    start = second_position
                    end = first_position

                f.write(gene_name + ',' + line.split(',')[0] + ',' + start + ',' +
                        end + ',' + line.split(',')[4]
                        )