from flask import Flask, render_template, session, request, make_response, redirect, url_for
from datetime import datetime
from os import mkdir
from authentication import Authenticator


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
        file= request.files.get('file')
        file.save(f'./static/{cookie_created}/{file.filename}')

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port= 888, host= 'localhost', debug= True)


















