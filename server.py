import os

from flask import Flask, render_template, session, request, make_response, redirect, url_for, jsonify, send_file
from datetime import datetime
import os
from os import mkdir
from os.path import isfile, join
from authentication import Authenticator
import extractor
import json
from process_yolo import process_yolo
from rescale import rescale
from labelsZipper import getLabels


app= Flask(__name__)

auth= Authenticator('5fkLAwr83MYxc445Tejvbdjn5Uo5SaWr5KbTZ812p93gc7403aQw')

host_url= 'http://localhost:5555/'


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
            mkdir(f'./static/{id}/labels')
            os.system(f'cp ./static/default/eagle.jpg ./static/{id}/eagle.jpg')
        except FileExistsError:
            pass
        return resp

    if auth.validate(cookie_id, cookie_key):
        return redirect(url_for('index') + '0')

    resp= make_response(redirect(url_for('index')))
    resp.set_cookie('created', '', expires= 0)
    resp.set_cookie('key', '', expires= 0)
    return resp


@app.route('/<im>')
def image(im):
    im= int(im)
    cookie_id = request.cookies.get('created')
    cookie_key = request.cookies.get('key')
    try:
        if auth.validate(cookie_id, cookie_key):
            dir= [f for f in os.listdir(f'./static/{cookie_id}') if isfile(join(f'./static/{cookie_id}', f))]
            im_path= dir[im]
            url_next= host_url + str(im + 1 if im < len(dir)-1 else len(dir)-1)
            url_previous= host_url + str(im-1 if im > 0 else 0)
            print(url_previous)
            return render_template(
                'index.html',
                id= cookie_id,
                image_path= f'./static/{cookie_id}/{im_path}',
                url_next= url_next,
                url_previous= url_previous,
                label_download= host_url + 'download'
            )
    except BaseException:
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('created', '', expires=0)
        resp.set_cookie('key', '', expires=0)
        return resp


@app.route('/add', methods= ['GET', 'POST'])
def addLabel():
    id= request.cookies.get('created')
    received_data= dict(request.args)
    dataS= list(received_data.keys())[0]
    yolo_data= json.loads(dataS)
    process_yolo(id, yolo_data)
    resp= make_response(jsonify({'status': 'SUCCESS'}))
    resp.status_code= 200
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


@app.route('/download')
def download():
    cookie_id= request.cookies.get('created')
    key= request.cookies.get('key')
    if auth.validate(cookie_id, key):
        zip_name= getLabels(cookie_id)
        return send_file(zip_name, as_attachment= True)


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
