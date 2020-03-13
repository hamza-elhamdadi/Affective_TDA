import getData

import os, fnmatch
import json
import webbrowser
import csv

from flask import Flask, request, render_template, send_from_directory, send_file

app = Flask(__name__)

datasets = []

with open('Data/bottleneck_dissimilarities.csv', 'r') as file:
    csv_file = csv.reader(file, delimiter=',')
    next(csv_file)
    csv_formatted = map(lambda elem : [elem[0], elem[1], float(elem[2])], csv_file)
    for row in csv_formatted:
        datasets.append(list(row))

webbrowser.open_new_tab('http://127.0.0.1:5000/')

def error(err):
    print(err)

@app.route('/')
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

@app.route('/data', methods=['GET'])
def get_data():
    emType = request.args.get('embeddingType')
    emID = request.args.get('emotionID')
    dMetric = request.args.get('differenceMetric')

    return getData.get_data(dMetric, emType, emID)
    