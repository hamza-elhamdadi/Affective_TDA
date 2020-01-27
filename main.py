from ripser import ripser
from persim import plot_diagrams
import nmf
import json
import numpy as np

data = []
mat = []

csv_file = open('Data/000.csv', 'r')
json_file = open('Data/000matrix.json', 'w')

next(iter(csv_file))

for line in csv_file:
    line_arr = line.split(',')
    data.append([float(line_arr[0]),float(line_arr[1]),float(line_arr[2])])
    
for i in range(len(data)):
    row = []
    for j in range(len(data)):
        row.append(nmf.distance(data[i],data[j],3))
    mat.append(row)

dissimilarity_string = json.dumps(mat)

json_file.write(dissimilarity_string)

diagrams = ripser(np.asarray(mat), distance_matrix = True)['dgms']

plot_diagrams(diagrams, show = True)