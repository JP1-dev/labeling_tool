import zipfile
import os
import shutil


def extract(id, filename):
    with zipfile.ZipFile(f'./static/{id}/{filename}', 'r') as zip:
        dir_name= filename.split('.')[0]
        zip.extractall(f'./static/{id}')

    lstOfAllFiles= os.listdir(f'./static/{id}/{dir_name}')
    for element in lstOfAllFiles:
        shutil.move(f'./static/{id}/{dir_name}/{element}', f'./static/{id}/{element}')

    os.rmdir(f'./static/{id}/{dir_name}')
    os.remove(f'./static/{id}/{filename}')