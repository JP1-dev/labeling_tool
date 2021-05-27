import os

from flask import Flask, render_template, session, request, make_response, redirect, url_for
from datetime import datetime
from os import mkdir
from authentication import Authenticator
import extractor
import json


app= Flask(__name__)

auth= Authenticator('5fkLAwr83MYxc445Tejvbdjn5Uo5SaWr5KbTZ812p93gc7403aQw')

currentImage= {}

@app.route('/', methods=['GET', 'POST'])
def index():
    cookie_id= request.cookies.get('created')
    cookie_key= request.cookies.get('key')

    if cookie_id is None:
        resp= make_response(redirect(url_for('index')))
        id= str(request.remote_addr) + 'SEP' + str(datetime.now()).replace(' ', '-')
        resp.set_cookie('created', id)
        resp.set_cookie('key', auth.sign(id))

        try:
            mkdir(f'./static/{id}')
            currentImage[id]= 0
        except FileExistsError:
            pass
        return resp

    if auth.validate(cookie_id, cookie_key):
        try:
            allDirs= os.listdir(f'./static/{cookie_id}')
        except BaseException:
            allDirs= []

        if not allDirs:
            print('yeahhh')
            image_path= './static/default/fish.png'
            return render_template("index.html", id= cookie_id, image_path= image_path)

        else:
            print('mist')
            image_path= f'./static/{cookie_id}/{allDirs[currentImage[cookie_id]]}'
            return render_template("index.html", id= cookie_id, image_path= image_path)

    resp= make_response(redirect(url_for('index')))
    resp.set_cookie('created', '', expires= 0)
    resp.set_cookie('key', '', expires= 0)
    return resp


@app.route('/uploadZIP', methods=['GET', 'POST'])
def uploadZIP():
    cookie_created= request.cookies.get('created')
    cookie_key= request.cookies.get('key')

    if auth.validate(cookie_created, cookie_key):
        try:
            file= request.files.get('file')
            if file.filename.split('.')[1] != 'zip':
                raise BaseException

            file.save(f'./static/{cookie_created}/{file.filename}', )
            extractor.extract(cookie_created, file.filename)

        except BaseException as err:
            return f"""<h3>error occured {err}</h3> <a href="{url_for('index')}">back to index</a>"""

    return redirect(url_for('index'))


@app.route('/add', methods= ['GET', 'POST'])
def addLabel():
    received_data= dict(request.args)
    dataS= list(received_data.keys())[0]
    yolo_data= json.loads(dataS)

    return "STATUS200"


@app.route('/nextImage', methods= ['GET', 'POST'])
def nextImage():
    current= request.args.get('current')
    id= request.cookies.get('created')
    allDir= os.listdir(f'./static/{id}')
    if int(current) + 1 < len(allDir):
        currentImage[id]+= 1
        return 'STATUS200'
    return 'last image reached'


if __name__ == '__main__':
    app.run(port= 5555, host= 'localhost', debug= True)





"""
lstOfAllImages= os.listdir(f'./static/{cookie_id}')
        image_path= './static/1/fish.png'
        if lstOfAllImages and request.method == 'POST':
            image_path= f'./static/{cookie_id}/{lstOfAllImages[0]}'
            currentImage= request.args.get('current')
            if currentImage is not None:
                for index, images in enumerate(lstOfAllImages):
                    if images == currentImage:
                        if index < len(lstOfAllImages):
                            image_path= lstOfAllImages[index+1]
                        else:
                            image_path= lstOfAllImages[index]
"""