import gzip
import sys
import os
import re

# Input: one gff file
# Output: adjusted gff file

input_path = 'hmmsearch_intersection/'
output_path = 'hmmsearch_intersection/'
result = os.listdir(input_path)


# # Check which genes are present in all species (but inside one species just once)
intersection_result = []

long_list = open(input_path + 'all_presence_once_good.txt').readlines()

unique_long_list = list(set(long_list))

for gene in unique_long_list:
    print('count: ', long_list.count(gene))
    if long_list.count(gene) >= 928: #should be 928
        intersection_result.append(gene)

# Save output file
output_file = open(output_path + 'genes_in_928_species.txt', 'w')

for species in intersection_result:
    output_file.write(species)