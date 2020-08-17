from sklearn.manifold import MDS, TSNE, trustworthiness
from matplotlib import pyplot as plt
from scipy.spatial import distance
from os import path
import csv, json, numpy as np

def getTrustworthiness(original, embedding):
    return trustworthiness(X=original, X_embedded=embedding, metric="precomputed")

length_of_file = 670

key = {
    "Angry": (0,112),
    "Disgust": (112,220),
    "Fear": (220,331),
    "Happy": (331,442),
    "Sad": (442,556),
    "Surprise": (556,length_of_file)
}

actionUnitsKey = {
    "leftEye": (0,7),
    "rightEye": (8,15),
    "leftEyebrow": (16,25),
    "rightEyebrow": (26,35),
    "nose": (36,47),
    "mouth": (48,67),
    "jawline": (68,82)
}

valid = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']

def shepardsDiagram(matrix, embedding, dimension, picName):
    m = matrix.flatten()
    emb = list(enumerate(embedding.flatten())) if dimension == 1 else embedding

    d = [distance.euclidean(d,e) for d in emb for e in emb]

    plt.scatter(m, d)
    plt.savefig(picName)

def embed(etype, dimension, perp):
    return {
        'mds': MDS(n_components=dimension,dissimilarity='precomputed', random_state=0),
        'tsne': TSNE(n_components=dimension,metric='precomputed', perplexity=perp, random_state=None)
    }.get(etype)

def dissMatFromHeraOut(lines, dim):
    dissimilarity = np.zeros(shape=(dim,dim))
    for vals in lines:
        dissimilarity[vals[0]][vals[1]] = vals[2]
        dissimilarity[vals[1]][vals[0]] = vals[2]
    return dissimilarity

def map_names(string):
    vals = string.split('_')
    return key[vals[-2]][0] + int(vals[-1])

def mapping_lambda(row):
    row[0] = map_names(row[0])
    row[1] = map_names(row[1])
    row[2] = float(row[2])
    return row

def extend_frameNumber(frameNumber):    
    return "{0:0=3d}".format(int(frameNumber))

def get_embedding_data(section_list, differenceMetric, embeddingType, emotionID, nonMetric, perplexity, dimension, retDiss):
    sections = '_'.join(section_list)
    filepath = f'../outputData/metric/F001/subsections/dissimilarities/{differenceMetric}/{sections}.csv' if nonMetric == 'metric' else '../outputData/nonmetric/F001/subsections/dissimilarities/{}/{}.csv'.format(differenceMetric, sections.replace('mouth', 'innermouth_outermouth'))

    with open(filepath, 'r') as file:
        lines = file.readlines()

    dissimilarities = list(map(lambda elem : list(map(lambda l: float(l), elem.split(' ')[:-1] if nonMetric == 'metric' else elem.split(' '))), lines))

    if retDiss:
        return dissimilarities

    embedding = embed(embeddingType, dimension, int(perplexity))

    #with open(f'../cache/{nonMetric}/F001/trustworthiness/{differenceMetric}_{embeddingType}_{sections}_{emotionID}_{dimension}D.json', 'w') as file:
    #    file.write(getTrustworthiness(dissimilarities, embedding))

    data = embedding.fit_transform(np.asmatrix(dissimilarities))[key[emotionID][0]:key[emotionID][1]]

    if dimension == 1:
        array = list(map(lambda e : float(e[0]), data))
        return [{'x': i, 'y': array[i]} for i in range(len(array))]
    else:
        array = list(map(lambda e : list(map(lambda l: float(l), e)), data))
        return list(map(lambda l: {'x':l[0], 'y':l[1]}, array))

def get_face_data(section_list, personData, emotion, frameNumber):
    frame = extend_frameNumber(frameNumber)
    file_path = f'../Data/{personData}/{emotion}/{frame}.bnd'

    with open(file_path, 'r') as file:
        data = file.readlines()
        data = list(map(lambda line : line[:-1].split(' '), data))
        data = list(map(lambda li : li[1:-1], data))
        data = list(map(lambda li : list(map(lambda e : float(e), li)), data))
        data = list(map(lambda pair : {"x":pair[0], "y":pair[1]}, data))

    ret = []

    for subsection in section_list:
        pointRange = actionUnitsKey.get(subsection)
        ret += data[pointRange[0]:pointRange[1]+1]

    return ret

def get_persistence_diagram(section_list, personData, emotion, frameNumber, nonMetric):
    frame = extend_frameNumber(frameNumber)
    sections = '_'.join(section_list)

    h_0 = []
    h_1 = []

    if nonMetric == 'metric':
        filepath = f'../outputData/metric/F001/subsections/persistence/{sections}/persistence_diagram_{sections}_{emotion}_{frame}.txt'

        with open(filepath, 'r') as file:
            lines = file.readlines()

            for line in lines:
                coords = line.split(' ')
                
                coordObj = {
                    'x':float(coords[0]),
                    'y':float(coords[1])
                }

                if(float(coords[0]) == 0.0):
                    h_0.append(coordObj)
                else:
                    h_1.append(coordObj)
    else:
        sections = sections.replace('mouth', 'innermouth_outermouth')
        filepathH0 = f'../outputData/nonmetric/F001/subsections/persistence/h0/{sections}/persistence_diagram_{sections}_{emotion}_{frame}.txt'
        filepathH1 = f'../outputData/nonmetric/F001/subsections/persistence/h1/{sections}/persistence_diagram_{sections}_{emotion}_{frame}.txt'

        with open(filepathH0, 'r') as file:
            lines = file.readlines()

            for line in lines:
                coords = line.split(' ')
                coordObj = {
                    'x':float(coords[0]),
                    'y':float(coords[1])
                }
                h_0.append(coordObj)

        with open(filepathH1, 'r') as file:
            lines = file.readlines()

            for line in lines:
                coords = line.split(' ')
                coordObj = {
                    'x':float(coords[0]),
                    'y':float(coords[1])
                }
                h_1.append(coordObj)
 
    return [h_0, h_1]


