import zipfile
import os
import shutil


def extract(id, filename):
    with zipfile.ZipFile(f'./static/{id}/{filename}', 'r') as zip:
        dir_name= filename.split('.')[0]
        zip.extractall(f'./static/{id}/{dir_name}')

    lstOfAllFiles= os.listdir(f'./static/{id}/{dir_name}/images')
    for element in lstOfAllFiles:
        shutil.move(f'./static/{id}/{dir_name}/images/{element}', f'./static/{id}/{element}')
        txtFilename= f"./static/{id}/labels/{element.replace(element.split('.')[-1], 'txt')}"
        open(txtFilename, 'a').close()
    os.remove(f'./static/{id}/eagle.jpg')
    os.rmdir(f'./static/{id}/{dir_name}/images')
    os.rmdir(f'./static/{id}/{dir_name}')
    os.remove(f'./static/{id}/{filename}')


