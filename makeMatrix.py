from ripser import ripser
import nmf
import json
import numpy as np
import os

filesindir = nmf.getFileNames('../Data/F001', '.bnd')
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']
subsections = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'mouth', 'jawline']

def build(filename, emotion, section_list):
    addition = ''
    for subsection in section_list:
        addition = addition + subsection + '_'
    
    mat = nmf.calculateDissimilaritiesFromCSV(filename, section_list, False)
    diagrams = ripser(np.asarray(mat), distance_matrix = True)['dgms']

    newdiagrams = diagrams[0].tolist() + diagrams[1].tolist()

    matjson = json.dumps(mat)
    diagramsjson = json.dumps(diagrams[0].tolist())

    fileinfo = nmf.get_frame_number(filename, False)[0]

    if len(section_list) == 0:
        distance_json = open('Data/F001/json/dissimilarities/' + emotion + '_' + fileinfo + '_distance_matrix.json', 'w')
        persistence_json = open('Data/F001/json/persistence/persistence_diagram_' + emotion + '_' + fileinfo + '.json', 'w')
        persistence_txt = open('Data/F001/persistence/persistence_diagram_' + emotion + '_' + fileinfo + '.txt', 'w')
    else:
        distance_json = open('Data/F001/subsections/json/dissimilarities/' + addition + emotion + '_' + fileinfo + '_distance_matrix.json', 'w')
        persistence_json = open('Data/F001/subsections/json/persistence/persistence_diagram_' + addition + emotion + '_' + fileinfo + '.json', 'w')
        persistence_txt = open('Data/F001/subsections/persistence/persistence_diagram_' + addition + emotion + '_' + fileinfo + '.txt', 'w')

    distance_json.write(matjson)
    persistence_json.write(diagramsjson)

    for i in newdiagrams:
        persistence_txt.write(str(i[0]) + ' ' + str(i[1]) + '\n')

def main():
    for filename in filesindir:
        for emotion in emotions:
            for section in subsections:
                build(filename, emotion, [section])

if __name__ == '__main__':
    main()