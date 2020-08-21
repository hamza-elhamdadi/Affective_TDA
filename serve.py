import getData, json, webbrowser, csv, subprocess as sp
from os import path
import os

from flask import Flask, request, render_template, send_from_directory, send_file

app = Flask(__name__)

emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']
subsections = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'mouth', 'jawline']
slidevalues = ['slideValue1', 'slideValue2', 'slideValue3', 'slideValue4', 'slideValue5', 'slideValue6']

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

@app.route('/preprocessing', methods=['GET'])
def preprocess():
    return []

@app.route('/clear_cache', methods=['GET'])
def clear_cache():
    eType = request.args.get('embeddingType')
    diff = request.args.get('differenceMetric')
    nm = request.args.get('nonMetric')
    dim = request.args.get('dimension')
    arguments = list(filter(lambda l: l != None, [request.args.get(sec) for sec in subsections]))
    sections = '_'.join(arguments)
    requests = [int(request.args.get(x)) for x in emotions]
    filenameStart = f'../cache/{nm}/F001/{diff}_{eType}_{sections}_'

    for i in range(len(requests)):
        if requests[i] == 1:
            #os.remove(f'{filenameStart}{emotions[i]}.json')
            os.remove(f'{filenameStart}{emotions[i]}_{dim}D.json')
    return json.dumps('Pre-Computed t-SNE Data Cleared')

@app.route('/embedding', methods=['GET'])
def get_embedding_data():
    emType = request.args.get('embeddingType')
    dMetric = request.args.get('differenceMetric')
    perp = request.args.get('perplexity')
    sections = [request.args.get(sec) for sec in subsections]
    dim = int(request.args.get('dimension'))
    nm = request.args.get('nonMetric')
    section_list = list(filter(lambda elem : True if elem != None else False, sections))
    secs = '_'.join(section_list)

    emotionFile = f'../cache/{nm}/F001/{dMetric}_{emType}_{secs}_'

    data = []
    currEmotions = []
    requests = [int(request.args.get(x)) for x in emotions]

    for i in range(len(requests)):
        if requests[i] == 1:
            currEmotions.append(emotions[i])
            emotionFile = f'{emotionFile}{emotions[i]}_'
        else:
            currEmotions.append(None)

    emotionFile = f'{emotionFile}{dim}D.json'

    if not path.exists(emotionFile):
        data = getData.get_embedding_data(section_list, dMetric, emType, currEmotions, request.args.get('nonMetric'), perp, dim, False)
        with open(emotionFile, 'w') as file:
            file.write(json.dumps(data))
    else:
        with open(emotionFile, 'r') as file:
            data = json.load(file)

    return json.dumps(data)

@app.route('/face', methods=['GET'])
def get_face_data():
    frameNumbers = [request.args.get(slidevalues[i]) for i in range(len(slidevalues))]

    sections = [request.args.get(sec) for sec in subsections]
    section_list = list(filter(lambda elem : True if elem != None else False, sections))
    secs = '_'.join(section_list)

    nm = request.args.get('nonMetric')

    fileNameStart = f'../cache/{nm}/F001/FaceData/'

    data = []
    requests = [int(request.args.get(x)) for x in emotions]

    for i in range(len(requests)):
        if requests[i] == 1:
            emotionFile = f'{fileNameStart}{frameNumbers[i]}_{secs}_{emotions[i]}.json'
            if path.exists(emotionFile):
                with open(emotionFile, 'r') as file:
                    data.append(json.load(file))
            else:
                data.append(getData.get_face_data(section_list, 'F001', emotions[i], frameNumbers[i]))
                with open(emotionFile, 'w') as file:
                    file.write(json.dumps(data[-1]))
        else:
            data.append(None)

    return json.dumps(data)

@app.route('/persistence', methods=['GET'])
def get_persistence_diagram():
    frameNumbers = [request.args.get(slidevalues[i]) for i in range(len(slidevalues))]

    sections = [request.args.get(sec) for sec in subsections]
    section_list = list(filter(lambda elem : True if elem != None else False, sections))

    data = []
    requests = [int(request.args.get(x)) for x in emotions]

    for i in range(len(requests)):
        if requests[i] == 1:
            data.append(getData.get_persistence_diagram(section_list, 'F001', emotions[i], frameNumbers[i], request.args.get('nonMetric')))
        else:
            data.append(None)
    
    return json.dumps(data).replace('Infinity', '"Infinity"')

app.run(host='0.0.0.0', port=5000)
