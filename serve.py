import os, fnmatch
import json
import webbrowser

from flask import Flask, request, render_template, send_from_directory, send_file

app = Flask(__name__)

datasets = []

with open('Data/bottleneck_dissimilarities.csv', 'r') as file:
    next(iter(file))
    for line in file:
        datasets.append(line.split(','))

webbrowser.open_new_tab('http://127.0.0.1:5000/')

def error(err):
    print(err)

@app.route('/', methods=['POST', 'GET'])
def return_index():
    print(str(request.form.get('embeddingType'))) 
    print(str(request.form.get('emotionID')))
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