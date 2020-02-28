from sklearn.manifold import MDS, TSNE, Isomap
import operator as op
import numpy as np
import nmf

###############################
#            TODO             #
###############################

# import csv

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

length_of_file = 666
embeddings = ['MDS', 'TSNE', 'Isomap']
bottleneck_values = []
wasserstein_values = []

with open('Data/bottleneck_values.csv', 'r') as file:
    bottleneck_input = file.readlines()
    for line in bottleneck_input:
        vals = line.split(',')
        value1 = False
        value2 = False
        for string in valid:
            if string in vals[0]:
                value1 = True
            if string in vals[1]:
                value2 = True
        if not value1 or not value2:
            continue
        bottleneck_values.append([map_names(vals[0]),map_names(vals[1]),float(vals[2])])
    

with open('Data/wasserstein_values.csv', 'r') as file:
    wasserstein_input = file.readlines()
    for line in wasserstein_input:
        vals = line.split(',')
        value1 = False
        value2 = False
        for string in valid:
            if string in vals[0]:
                value1 = True
            if string in vals[1]:
                value2 = True
        if not value1 or not value2:
            continue
        wasserstein_values.append([map_names(vals[0]),map_names(vals[1]),float(vals[2])])

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