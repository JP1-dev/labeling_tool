from flask import Flask, render_template, session, request, make_response, redirect, url_for
from datetime import datetime
from os import mkdir
from authentication import Authenticator
import extractor
import json


app= Flask(__name__)

auth= Authenticator('5fkLAwr83MYxc445Tejvbdjn5Uo5SaWr5KbTZ812p93gc7403aQw')


@app.route('/')
def index():
    cookie_id= request.cookies.get('created')
    cookie_key= request.cookies.get('key')

    if cookie_id is None:
        resp= make_response(redirect(url_for('index')))
        id= str(request.remote_addr) + 'SEP' + str(datetime.now())
        resp.set_cookie('created', id)
        resp.set_cookie('key', auth.sign(id))

        try:
            mkdir(f'./static/{id}')
        except FileExistsError:
            pass
        return resp

    if auth.validate(cookie_id, cookie_key):
        return render_template('index.html', id= cookie_id)

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

            file.save(f'./static/{cookie_created}/{file.filename}')
            extractor.extract(cookie_created, file.filename)

        except BaseException as err:
            return f"""<h3>error occured {err}</h3> <a href="{url_for('index')}">back to index</a>"""

    return redirect(url_for('index'))


@app.route('/add', methods= ['GET', 'POST'])
def addLabel():
    received_data= dict(request.args)
    dataS= list(received_data.keys())[0]
    yolo_data= json.loads(dataS)

    return "STATUS 200"


if __name__ == '__main__':
    app.run(port= 888, host= 'localhost', debug= True)






