import getData, json, webbrowser, csv
from os import path

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

@app.route('/embedding', methods=['GET'])
def get_embedding_data():
    emType = request.args.get('embeddingType')
    dMetric = request.args.get('differenceMetric')
    sections = [request.args.get(sec) for sec in subsections]

    section_list = list(filter(lambda elem : True if elem != None else False, sections))
    secs = '_'.join(section_list)

    fileNameStart = f'../cache/metric/F001/{dMetric}_{emType}_{secs}_'

    data = []
    requests = [int(request.args.get(x)) for x in emotions]
        
    for i in range(len(requests)):
        if requests[i] == 1:
            emotionFile = f'{fileNameStart}{emotions[i]}.json'
            if path.exists(emotionFile):
                with open(emotionFile, 'r') as file:
                    data.append(json.load(file))
            else:
                data.append(getData.get_embedding_data(section_list, dMetric, emType, emotions[i]))
                with open(emotionFile, 'w') as file:
                    file.write(json.dumps(data[-1]))
        else:
            data.append(None)

    return json.dumps(data)

@app.route('/face', methods=['GET'])
def get_face_data():
    index = request.args.get('emotion')
    frameNumbers = [request.args.get(slidevalues[i]) for i in range(len(slidevalues))]
    frameNumber = frameNumbers[int(index)]

    sections = [request.args.get(sec) for sec in subsections]
    section_list = list(filter(lambda elem : True if elem != None else False, sections))
    secs = '_'.join(section_list)

    fileNameStart = f'../cache/metric/F001/FaceData/{frameNumber}_{secs}_'

    data = []
    requests = [int(request.args.get(x)) for x in emotions]

    for i in range(len(requests)):
        if requests[i] == 1:
            emotionFile = f'{fileNameStart}{emotions[i]}.json'
            if path.exists(emotionFile):
                with open(emotionFile, 'r') as file:
                    data.append(json.load(file))
            else:
                data.append(getData.get_face_data(section_list, 'F001', emotions[i], frameNumber))
                with open(emotionFile, 'w') as file:
                    file.write(json.dumps(data[-1]))
        else:
            data.append(None)

    return json.dumps(data)

@app.route('/persistence', methods=['GET'])
def get_persistence_diagram():
    index = request.args.get('emotion')
    frameNumbers = [request.args.get(slidevalues[i]) for i in range(len(slidevalues))]
    frameNumber = frameNumbers[int(index)]

    sections = [request.args.get(sec) for sec in subsections]
    section_list = list(filter(lambda elem : True if elem != None else False, sections))
    secs = '_'.join(section_list)

    data = []
    requests = [int(request.args.get(x)) for x in emotions]

    for i in range(len(requests)):
        if requests[i] == 1:
            data.append(getData.get_persistence_diagram(section_list, 'F001', emotions[i], frameNumber))
        else:
            data.append(None)
    
    return json.dumps(data).replace('Infinity', '"Infinity"')

