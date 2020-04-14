import getData
from os import path
import json
import webbrowser
import csv

from flask import Flask, request, render_template, send_from_directory, send_file

app = Flask(__name__)

emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']
subsections = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'mouth', 'jawline']

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

    fileNameStart = 'cache/F001/' + str(dMetric) + '_' + str(emType) + '_'

    data = []
    requests = [int(request.args.get(x)) for x in emotions]
    sectionVals = [int(request.args.get(x)) for x in subsections]
    section_list = []
    sections = ''
    for i in range(len(sectionVals)):
        if sectionVals[i] == 1:
            section_list.append(subsections[i])
    for subsection in section_list:
        sections += subsection + '_'
        
    
    for i in range(len(requests)):
        if requests[i] == 1:
            emotionFile = fileNameStart + sections + emotions[i] + '.json'
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
    frameNumber = request.args.get('slideValue')

    fileNameStart = 'cache/F001/FaceData/' + str(frameNumber)

    data = []
    requests = [int(request.args.get(x)) for x in emotions]
    sectionVals = [int(request.args.get(x)) for x in subsections]
    section_list = []
    sections = ''
    for i in range(len(sectionVals)):
        if sectionVals[i] == 1:
            section_list.append(subsections[i])
    for subsection in section_list:
        sections += subsection + '_'

    for i in range(len(requests)):
        if requests[i] == 1:
            emotionFile = fileNameStart + sections + emotions[i] + '.json'
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