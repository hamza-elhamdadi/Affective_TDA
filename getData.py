from sklearn.manifold import MDS, TSNE, Isomap
import numpy as np
import nmf
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

def get_data(differenceMetric, embeddingType, emotionID):
    values = []
    with open('Data/' + differenceMetric + '_values.csv', 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        next(csv_file)
        csv_formatted = map(lambda elem : mapping_lambda(elem), csv_file)
        for row in csv_formatted:
            if row[0] == '' or row[1] == '' or row[0] == 'F00' or row[1] == 'F00':
                continue
            values.append([map_names(row[0]),map_names(row[1]),float(row[2])])

    dissimilarities = nmf.dissMatFromHeraOut(values, length_of_file)

    if embeddingType == 'mds':
        embedding = MDS(n_components=1,dissimilarity='precomputed')
    elif embeddingType == 'tsne':
        embedding = TSNE(n_components=1,metric='precomputed')
    else:
        embedding = Isomap(n_components=1,metric='precomputed')

    data = embedding.fit_transform(np.asmatrix(dissimilarities))

    arr = np.array2string(data).replace('\n', '').replace('[','').replace(']','').split(' ')
    arr = list(map(lambda e : float(e), filter(lambda e : e != '', arr)))

    if emotionID == 'angry':
        return json.dumps(arr[:112])
    elif emotionID == 'disgust':
        return json.dumps(arr[112:220])
    elif emotionID == 'fear':
        return json.dumps(arr[220:331])
    elif emotionID == 'happy':
        return json.dumps(arr[331:442])
    elif emotionID == 'sad':
        return json.dumps(arr[442:556])
    else:
        return json.dumps(arr[556:])