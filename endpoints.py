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
    return json.dumps(impl.new_file(filename, content))

@app.route('/upload-text', methods=['POST'])
def upload_text():
    data = request.form['data']
    filename = request.form['filename']
    return json.dumps(impl.new_file(filename, data))

@app.route('/upload-file', methods=['POST'])
def upload_file():
    for filename in request.files:
        f = request.files[filename]
        return json.dumps(impl.new_file(filename, f.stream.read()))
    return "{}"

@app.route('/upload-files', methods=['POST'])
def upload_files():
    request.get_data()
    hashcodes = []
    for filename in request.files:
        f = request.files[filename]
        h = impl.new_file(filename, f.stream.read())["hashcode"]
        hashcodes.append(h)
    return json.dumps({"hashcodes":hashcodes})

@app.route('/files/<path:hashcode>', methods=['GET'])
def r_files(hashcode):
    filename, content = impl.get_file(hashcode)
    if filename != None:
        _, file_extension = os.path.splitext(filename)
        response = Response(content, mimetype = ext_to_type(file_extension))
        response.headers['Content-Disposition'] = 'attachment; filename=' + filename
        return response
    return abort(404)

@app.route('/view/<path:hashcode>', methods=['GET'])
def r_view(hashcode):
    filename, content = impl.get_file(hashcode)
    if filename != None:
        _, file_extension = os.path.splitext(filename)
        response = Response(content, mimetype = ext_to_type(file_extension))
        return response
    return abort(404)

@app.route('/size/<path:hashcode>', methods=['GET'])
def r_size(hashcode):
    filename, content = impl.get_file(hashcode)
    if filename != None:
        return str(len(content))
    return abort(404)

