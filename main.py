from ripser import ripser
from persim import plot_diagrams
import nmf
import json
import numpy as np
import os

filename = input('Please enter the name of the file:')

mat = nmf.calculateDissimilaritiesFromCSV(filename)
diagrams = ripser(np.asarray(mat), distance_matrix = True)['dgms']

distance_json = open('Data/json/dissimilarities/' + filename + '_distance_matrix.json', 'w')
persistence_json = open('Data/json/persistence/persistence_diagram_' + filename[8:11] + '.json', 'w')
persistence_txt = open('Data/persistence/persistence_diagram_' + filename[8:11] + '.txt', 'w')

distance_json.write('{\n\t"dissimilarities": ' + json.dumps(mat) + '\n}')
persistence_json.write(json.dumps(diagrams))

for i in list(diagrams[0] + diagrams[1]):
    persistence_txt.write(str(i[0]) + ' ' + str(i[1]) + '\n')