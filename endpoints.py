'''
Functions to handle incoming web requests,
then appeal to implentation to do the work.
'''

from flask import render_template
from flask import request
from flask import abort

from server import app
from mime import ext_to_type
from flask import Response

import time

import implementation
import database
import base64
import os
import re
import json

db = database.Database("sqlite:///testing.db")
impl = implementation.Implementation(db.models, db.session)

def file_extension(filename):
    return filename.split('.')[-1]

@app.route('/')
def r_index():
    return render_template('index.html')

@app.route('/upload-base64', methods=['POST'])
def upload_base64():
    filename = request.form['filename']
    content = base64.b64decode(re.findall("base64,(.*)", request.form['content'])[0])
    time.sleep(3) # DEBUG CODE
    return impl.new_file(filename, content)


@app.route('/upload-text', methods=['POST'])
def upload_text(username, projectslug):
    data = request.form['data']
    filename = request.form['filename']
    impl.new_file(filename, data)
    return json.dumps({"status":"okay"})


@app.route('/files/<path:hashcode>', methods=['GET'])
def r_files(hashcode):
    filename, content = impl.get_file(hashcode)

    if filename != None:
        _, file_extension = os.path.splitext(filename)
        response = Response(content, mimetype = ext_to_type(file_extension))
        response.headers['Content-Disposition'] = 'attachment; filename=' + filename
        return response
    else:
        return abort(404)

    return impl.files(hashcode)


