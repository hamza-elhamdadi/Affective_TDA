from sklearn.manifold import MDS, TSNE, Isomap
from os import path
import hera, csv, json, numpy as np

length_of_file = 684

key = {
    "Angry": (0,112),
    "Disgust": (112,220),
    "Fear": (220,331),
    "Happy": (331,442),
    "Sad": (442,556),
    "Surprise": (556,length_of_file)
}

embeddings = {
    "mds":MDS(n_components=1,dissimilarity='precomputed', random_state=0),
    "tsne":TSNE(n_components=1,metric='precomputed'),
    "isomap":Isomap(n_components=1,metric='precomputed')
}

actionUnitsKey = {                                                                                                                                              # dictionary mapping parts of face
    "leftEye": (0,7),                                                                                                                                           # to a subset of the Action Units list
    "rightEye": (8,15),                                                                                 
    "leftEyebrow": (16,25),
    "rightEyebrow": (26,35),
    "nose": (36,47),
    "mouth": (48,67),
    "jawline": (68,82)
}

valid = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']

def min_max(subsection):
    if subsection in actionUnitsKey.keys():                                                                                                                     # check if the subsection is valid
        return actionUnitsKey[subsection]                                                                                                                       # return the value for the subsection key
    else:                                                                                                                                                       # if it's invalid
        return None                                                                                                                                             # return None

def dissMatFromHeraOut(file_lines, length_of_file):
    dissimilarity = np.zeros(shape=(length_of_file,length_of_file))
    for vals in file_lines:
        dissimilarity[vals[0]][vals[1]] = vals[2]
        dissimilarity[vals[1]][vals[0]] = vals[2]
    return dissimilarity

def map_names(string):
    vals = string.split('_')
    return key[vals[-2]][0] + int(vals[-1])

def mapping_lambda(row):
    if row[2] == '' or row[2] == 'inf':
        return row
    else:
        return [row[0], row[1], float(row[2])]

def extend_frameNumber(frameNumber):
    frame = str(frameNumber)
    if len(frame) == 1:
        frame = '00' + frame
    elif len(frame) == 2:
        frame = '0' + frame
    
    return frame

def get_embedding_data(section_list, differenceMetric, embeddingType, emotionID):
    sections = '_'.join(section_list)
    filepath = f'Data/F001/subsections/dissimilarities/{differenceMetric}/{sections}_{differenceMetric}_dissimilarities.csv'

    if not path.exists(filepath):
        print(filepath)
        hera.hera(section_list)

    with open(filepath, 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        next(csv_file)
        csv_formatted = map(lambda elem : mapping_lambda(elem), csv_file)
        values = [[map_names(row[0]),map_names(row[1]),float(row[2])] for row in csv_formatted]

    dissimilarities = dissMatFromHeraOut(values, length_of_file)
    embedding = embeddings[embeddingType]

    data = embedding.fit_transform(np.asmatrix(dissimilarities))

    arr = np.array2string(data).replace('\n', '').replace('[','').replace(']','').split(' ')
    arr = list(map(lambda e : float(e), filter(lambda e : e != '', arr)))

    array = arr[key[emotionID][0]:key[emotionID][1]]
    
    return [{'x':i,'y':array[i]} for i in range(len(array))]

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
        pointRange = min_max(subsection)
        ret += data[pointRange[0]:pointRange[1]+1]

    return ret

def get_persistence_diagram(section_list, personData, emotion, frameNumber):
    frame = extend_frameNumber(frameNumber)
    sections = '_'.join(section_list)
    filepath = f'./Data/F001/subsections/persistence/{sections}/persistence_diagram_{sections}_{emotion}_{frame}.txt'

    h_0 = []
    h_1 = []

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

    return [h_0, h_1]


