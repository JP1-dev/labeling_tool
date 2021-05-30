import os

from flask import Flask, render_template, session, request, make_response, redirect, url_for
from datetime import datetime
from os import mkdir
from authentication import Authenticator
import extractor
import json
import os

app= Flask(__name__)

auth= Authenticator('5fkLAwr83MYxc445Tejvbdjn5Uo5SaWr5KbTZ812p93gc7403aQw')



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
            os.system(f'cp ~/coding/Python/basic/bus.jpg ~/coding/Python/labeling_tool/static/{id}/bus.jpg')
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
    if auth.validate(cookie_id, cookie_key) or True:
        dir= os.listdir(f'./static/{cookie_id}')
        im_path= dir[im]
        url_next= f'http://localhost:5555/{im + 1 if im < len(dir)-1 else len(dir)-1}'
        url_previous= f'http://localhost:5555/{im-1 if im > 0 else 0}'
        print(url_previous)
        return render_template(
            'index.html',
            id= cookie_id,
            image_path= f'./static/{cookie_id}/{im_path}',
            url_next= url_next,
            url_previous= url_previous
        )


@app.route('/add', methods= ['GET', 'POST'])
def addLabel():
    received_data= dict(request.args)
    dataS= list(received_data.keys())[0]
    yolo_data= json.loads(dataS)

    return "STATUS200"


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