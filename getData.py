from sklearn.manifold import MDS, TSNE, Isomap
from os import path
import numpy as np
import nmf
import hera
import csv
import json

key = {
    "Angry": 0,
    "Disgust": 112,
    "Fear": 220,
    "Happy": 331,
    "Sad": 442,
    "Surprise": 556,
}
valid = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']
length_of_file = 666

def map_names(string):
    vals = string.split('_')
    return key[vals[0]] + int(vals[1])

def mapping_lambda(row):
    if row[2] == '' or row[2] == 'inf':
        return row
    else:
        return [row[0], row[1], float(row[2])]


def get_embedding_data(section_list, differenceMetric, embeddingType, emotionID):
    values = []

    if len(section_list) == 0:
        filepath = 'Data/F001/' + differenceMetric + '_values.csv'
    else:
        sections = ''
        for subsection in section_list:
            sections += subsection + '_'
        filepath = 'Data/F001/subsections/' + sections + differenceMetric + '_values.csv'

    if not path.exists(filepath):
        print('it dont exist')
        hera.hera(section_list)

    with open(filepath, 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        next(csv_file)
        csv_formatted = map(lambda elem : mapping_lambda(elem), csv_file)
        for row in csv_formatted:
            if row[0] == '' or row[1] == '' or row[0] == 'F00' or row[1] == 'F00':
                continue
            values.append([map_names(row[0]),map_names(row[1]),float(row[2])])

    dissimilarities = nmf.dissMatFromHeraOut(values, length_of_file)

    if embeddingType == 'mds':
        embedding = MDS(n_components=1,dissimilarity='precomputed', random_state=0)
    elif embeddingType == 'tsne':
        embedding = TSNE(n_components=1,metric='precomputed')
    else:
        embedding = Isomap(n_components=1,metric='precomputed' )

    data = embedding.fit_transform(np.asmatrix(dissimilarities))

    arr = np.array2string(data).replace('\n', '').replace('[','').replace(']','').split(' ')
    arr = list(map(lambda e : float(e), filter(lambda e : e != '', arr)))

    ret = []

    if emotionID == 'Angry':
        array = arr[key['Angry']:key['Disgust']]
    elif emotionID == 'Disgust':
        array = arr[key['Disgust']:key['Fear']]
    elif emotionID == 'Fear':
        array = arr[key['Fear']:key['Happy']]
    elif emotionID == 'Happy':
        array = arr[key['Happy']:key['Sad']]
    elif emotionID == 'Sad':
        array = arr[key['Sad']:key['Surprise']]
    else:
        array = arr[key['Surprise']:]
    
    for i in range(len(array)):
        obj = {'x':i, 'y':array[i]}
        ret.append(obj)
    
    return ret

def get_face_data(section_list, personData, emotion, frameNumber):
    frame = str(frameNumber)
    if len(frame) == 1:
        frame = '00' + frame
    elif len(frame) == 2:
        frame = '0' + frame
    file_path = '../Data/' + str(personData) + '/' + str(emotion) + '/' + frame + '.bnd'

    with open(file_path, 'r') as file:
        data = file.readlines()
        data = list(map(lambda line : line[:-1].split(' '), data))
        data = list(map(lambda li : li[1:-1], data))
        data = list(map(lambda li : list(map(lambda e : float(e), li)), data))
        data = list(map(lambda pair : {"x":pair[0], "y":pair[1]}, data))

    ret = []

    for subsection in section_list:
        pointRange = nmf.min_max(subsection)
        ret += data[pointRange[0]:pointRange[1]]

        return ret

