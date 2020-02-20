from ripser import ripser
import nmf
import json
import numpy as np
import os

filename = input('Please enter the name of the file:')
emotion = input('and the emotion:')

mat = nmf.calculateDissimilaritiesFromCSV(filename)
diagrams = ripser(np.asarray(mat), distance_matrix = True)['dgms']

distance_json = open('Data/json/dissimilarities/' + emotion + '_' + filename[-7:-4] + '_distance_matrix.json', 'w')
persistence_json = open('Data/json/persistence/persistence_diagram_' + emotion + '_' + filename[-7:-4] + '.json', 'w')
persistence_txt = open('Data/persistence/persistence_diagram_' + emotion + '_' + filename[-7:-4] + '.txt', 'w')

distance_json.write('{\n\t"dissimilarities": ' + json.dumps(mat) + '\n}')
persistence_json.write(json.dumps(diagrams[0].tolist()))
persistence_json.write(json.dumps(diagrams[1].tolist()))

for i in diagrams[0].tolist() + diagrams[1].tolist():
    persistence_txt.write(str(i[0]) + ' ' + str(i[1]) + '\n')