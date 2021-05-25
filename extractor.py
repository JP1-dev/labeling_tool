import zipfile
import os

def extract(id, filename):
    with zipfile.ZipFile(f'./static/{id}/{filename}', 'r') as zip:
        dir_name= filename.split('.')[0]
        zip.extractall(f'./static/{id}/{dir_name}')

    lstOfAllFiles= os.listdir(f'./static/{id}/{dir_name}')
    print(lstOfAllFiles)
    print('hallo')