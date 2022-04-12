import pathlib
import os

path = str(pathlib.Path(__file__).parent.resolve()) + '/'
result = os.listdir(path)

def change_fasta_name(file_name):
    if '_GeneCatalog' in file_name:
        species = file_name.split('_GeneCatalog')[0]
    elif '_Filtered' in file_name:
        species = file_name.split('_Filtered')[0]
    elif '_External' in file_name:
        species = file_name.split('_External')[0]
    elif '.filtered' in file_name:
        species = file_name.split('.filtered')[0]
    elif '.Filtered' in file_name:
        species = file_name.split('.Filtered')[0]
    elif '_GeneModels' in file_name:
        species = file_name.split('_GeneModels')[0]
    elif '_primary' in file_name:
        species = file_name.split('_primary')[0]
    elif '_Frozen' in file_name:
        species = file_name.split('_Frozen')[0]
    else:
        print(file_name)
        species = 'X'
    old_name = path + file_name
    if '.gff3.gz' in file_name:
        new_name = path + species + '.gff3.gz'
        os.rename(old_name, new_name)
    elif '.gff.gz' in file_name:
        new_name = path + species + '.gff.gz'
        os.rename(old_name, new_name)


files = []
for i in result:
    files.append(i)

counter = 0

for file in files:
    if file.endswith('.gz'):
        #print(counter)
        counter += 1
        change_fasta_name(file)