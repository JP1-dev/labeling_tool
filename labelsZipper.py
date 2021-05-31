from zipfile import ZipFile
import os
from os.path import basename
from datetime import datetime


def getLabels(id):
    now= datetime.now()
    filename= f'labels_{now.year}-{now.month}-{now.day}-{now.hour}-{now.second}.zip'

    with ZipFile(filename, 'w') as file:
        for folderName,_,filenames in os.walk(f'./static/{id}/labels'):
            for txt in filenames:
                filePath= os.path.join(folderName, txt)
                file.write(filePath, basename(filePath))
    return filename
