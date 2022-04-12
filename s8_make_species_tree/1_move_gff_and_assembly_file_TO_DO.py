import os

# abspath to a folder as a string
import shutil

dir = os.getcwd()

folders_to_remove = []

new_assembly_path = '/home/i.huitink_cbs-niob.local/h/data/copy_jgi/classes/assemblies'
new_gff_path = '/home/i.huitink_cbs-niob.local/h/data/copy_jgi/classes/gffs'

for root, dirs, files in os.walk(dir):
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