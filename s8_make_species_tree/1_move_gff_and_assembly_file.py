# The downloaded JGI files are structured according to the taxonomy
# This code puts all species GFF and fasta files into two separate folders
# Input are the downloaded JGI files in taxonomy order
# Output are two folders containing the GFF and fasta files

# Import packages
import os
import shutil

# Define the new folders
new_assembly_path = '/home/i.huitink_cbs-niob.local/h/data/copy_jgi/classes/assemblies'
new_gff_path = '/home/i.huitink_cbs-niob.local/h/data/copy_jgi/classes/gffs'

# Get current working directory
dir = os.getcwd()

folders_to_remove = []

# Loop over downloaded JGI data
for root, dirs, files in os.walk(dir):
    # The new GFF and fasta folder need to be skipped
    if root != '/home/i.huitink_cbs-niob.local/h/data/copy_jgi/classes/gffs' and root != '/home/i.huitink_cbs-niob.local/h/data/copy_jgi/classes/assemblies':
        for file in files:
            if file.endswith('gff.gz') or file.endswith('gff3.gz'):
                old_assembly_path = os.path.join(root, root, file)
                shutil.move(old_assembly_path, new_gff_path)
            elif file.endswith('fasta.gz'):
                old_gff_path = os.path.join(root, root, file)
                shutil.move(old_gff_path, new_assembly_path)
            else:
                print('Other end: ', file)
