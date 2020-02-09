from ripser import ripser
from persim import plot_diagrams
import nmf
import json
import numpy as np
import os

data = []
mat = []

filename = input('Please enter the name of the file:')

csv_file = open(filename, 'r')
json_file = open('Data/json/' + filename + 'matrix.json', 'w')
persistence_file = open('Data/persistence/persistence_diagram_' + filename[8:11] + '.txt', 'w')

next(iter(csv_file))

for line in csv_file:
    line_arr = line.split(' ')
    data.append([float(line_arr[1]),float(line_arr[2]),float(line_arr[3])])
    
for i in range(len(data)):
    row = []
    for j in range(len(data)):
        row.append(nmf.distance(data[i],data[j],3))
    mat.append(row)

dissimilarity_string = json.dumps(mat)

json_file.write('{\n\t"dissimilarities": ' + dissimilarity_string + '\n}')

diagrams = ripser(np.asarray(mat), distance_matrix = True)['dgms']

for i in list(diagrams[0]):
    persistence_file.write(str(i[0]) + ' ' + str(i[1]) + '\n')
for i in list(diagrams[1]):
    persistence_file.write(str(i[0]) + ' ' + str(i[1]) + '\n')
