import zipfile
import os
import shutil


def extract(id, filename):
    with zipfile.ZipFile(f'./static/{id}/{filename}', 'r') as zip:
        print(filename)
        dir_name= filename.split('.')[0]
        print('1')
        zip.extractall(f'./static/{id}/{dir_name}')
    print('2')
    print(dir_name)
    lstOfAllFiles= os.listdir(f'./static/{id}/{dir_name}')
    print('3')
    for element in lstOfAllFiles:
        print('ok')
        shutil.move(f'./static/{id}/{dir_name}/{element}', f'./static/{id}/{element}')
    print('4')
    os.rmdir(f'./static/{id}/{dir_name}')
    os.remove(f'./static/{id}/{filename}')


