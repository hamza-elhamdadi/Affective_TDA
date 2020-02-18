import os, fnmatch
import json

from flask import Flask, request, render_template, send_from_directory, send_file

app = Flask(__name__)

datasets = {}

data_dir = '../Data'
current_ds = []
for dataset in os.listdir(data_dir):
    if fnmatch.fnmatch(dataset, '*.bnd'):
        current_ds.append(dataset[:-4])
datasets["first"] = current_ds

def error(err):
    print(err)

@app.route('/')
def return_index():
    return send_file('index.html')

@app.route('/hello')
def hello():
    return 'hello, World!'

@app.errorhandler(404)
def page_notfound(error):
    print('Error: ' + str(error))
    return 'This page does not exist', 404

@app.route('/datasets', methods=['GET', 'POST'])
def get_datasets():
    return json.dumps(datasets)