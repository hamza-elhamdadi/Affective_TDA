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

def map_names(string):
    vals = string.split('_')
    return key[vals[0]] + int(vals[1])

def mapping_lambda(row):
    if row[2] == '' or row[2] == 'inf':
        return row
    else:
        return [row[0], row[1], float(row[2])]

length_of_file = 666
embeddings = ['MDS', 'TSNE', 'Isomap']
bottleneck_values = []
wasserstein_values = []

with open('Data/F001/bottleneck_values.csv', 'r') as file:
    csv_file = csv.reader(file, delimiter=',')
    next(csv_file)
    csv_formatted = map(lambda elem : mapping_lambda(elem), csv_file)
    for row in csv_formatted:
        if row[0] == '' or row[1] == '' or row[0] == 'F00' or row[1] == 'F00':
            continue
        bottleneck_values.append([map_names(row[0]),map_names(row[1]),float(row[2])])
    

with open('Data/F001/wasserstein_values.csv', 'r') as file:
    csv_file = csv.reader(file, delimiter=',')
    next(csv_file)
    csv_formatted = map(lambda elem : mapping_lambda(elem), csv_file)
    for row in csv_formatted:
        if row[0] == '' or row[1] == '' or row[0] == 'F00' or row[1] == 'F00':
            continue
        wasserstein_values.append([map_names(row[0]),map_names(row[1]),float(row[2])])

bottleneck_dissimilarities = nmf.dissMatFromHeraOut(bottleneck_values, length_of_file)
wasserstein_dissimilarities = nmf.dissMatFromHeraOut(wasserstein_values, length_of_file)
"""nmf.writeDissimilarityMatrix('Data/bottleneck_dissimilarities.txt', bottleneck_dissimilarities)"""
"""nmf.writeDissimilarityMatrix('Data/wasserstein_dissimilarities.txt', wasserstein_dissimilarities)"""

embedding_MDS = MDS(n_components=1,dissimilarity='precomputed')
embedding_TSNE = TSNE(n_components=1,metric='precomputed')
embedding_Isomap = Isomap(n_components=1,metric='precomputed')

###############################
#            TODO             #
###############################

# Consider perplexity


data_1 = [embedding_MDS.fit_transform(np.asmatrix(bottleneck_dissimilarities)), 
          embedding_TSNE.fit_transform(np.asmatrix(bottleneck_dissimilarities)), 
          embedding_Isomap.fit_transform(np.asmatrix(bottleneck_dissimilarities))]

data_2 = [embedding_MDS.fit_transform(np.asmatrix(wasserstein_dissimilarities)), 
          embedding_TSNE.fit_transform(np.asmatrix(wasserstein_dissimilarities)), 
          embedding_Isomap.fit_transform(np.asmatrix(wasserstein_dissimilarities))]

for i in range(3):
    nmf.saveSignal('bottleneck', embeddings[i], length_of_file, data_1[i])
    nmf.saveSignal('wasserstein', embeddings[i], length_of_file, data_2[i])
    arr_1 = np.array2string(data_1[i]).replace('\n', '').replace('[','').replace(']','').split(' ')
    arr_1 = list(map(lambda e : float(e), filter(lambda e : e != '', arr_1)))
    arr_2 = np.array2string(data_2[i]).replace('\n', '').replace('[','').replace(']','').split(' ')
    arr_2 = list(map(lambda e : float(e), filter(lambda e : e != '', arr_2)))
    with open('Data/F001/json/signalData/bottleneck_' + embeddings[i] + '_data.json', 'w') as file:
        file.write(json.dumps(arr_1))
        file.close()
    with open('Data/F001/json/signalData/wasserstein_' + embeddings[i] + '_data.json', 'w') as file:
        file.write(json.dumps(arr_2))
        file.close()