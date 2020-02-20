# functions for the nonmetric_data_sets project

import math
import numpy as np
import matplotlib.pyplot as plt
import os

pi = np.pi

####################################################################################################
#                                                                                                  #
#                                        General Functions                                         #
#                                                                                                  #
####################################################################################################

# Euclidean distance between two points (supports two and three dimensions)

def distance(p0, p1, dimension):
    if dimension == 2:
        temp_1 = p1[0]-p0[0]
        temp_2 = p1[1]-p0[1]
        temp_1 = temp_1*temp_1
        temp_2 = temp_2*temp_2
        return math.sqrt(temp_1 + temp_2)
    else:
        temp_1 = p1[0]-p0[0]
        temp_2 = p1[1]-p0[1]
        temp_3 = p1[2]-p0[2]
        temp_1 = temp_1*temp_1
        temp_2 = temp_2*temp_2
        temp_3 = temp_3*temp_3
        return math.sqrt(temp_1 + temp_2 + temp_3)

# create the metric dissimilarity matrix

def dissim_matrix(data):
    dissimilarities = []

    for i in range(0,len(data)):
        current_line = []

        for j in range(0,len(data)):
            current_line.append(distance(data[i],data[j]))
        
        dissimilarities.append(current_line)

    return np.asanyarray(dissimilarities)

# generate randomness values

def rand_vals(start, end, num_dp):
    return [np.random.uniform(start, end) for x in range(0,num_dp+1)]

# read dissimilarities from csv

def calculateDissimilaritiesFromCSV(filename):
    data = []
    mat = []

    csv_file = open(filename, 'r')

    next(iter(csv_file))

    for line in csv_file:
        line_arr = line.split(' ')
        data.append([float(line_arr[1]),float(line_arr[2]),float(line_arr[3])])
    
    for i in range(len(data)):
        row = []
        for j in range(len(data)):
            row.append(distance(data[i],data[j],3))
        mat.append(row)
    
    return mat

# dissimilarity matrix from hera output

def dissMatFromHeraOut(filename, length_of_file):
    with open(filename,'r') as file:
        next(iter(file))
        dissimilarity = np.zeros(shape=(length_of_file,length_of_file))
        for line in file:
            vals = line.split(',')
            dissimilarity[int(vals[0])][int(vals[1])] = float(vals[2])
            dissimilarity[int(vals[1])][int(vals[0])] = float(vals[2])
        return dissimilarity

def writeDissimilarityMatrix(filename, dissimilarity):
    with open(filename, 'w') as writefile:
        for row in dissimilarity:
            row = map(lambda val: str(val), row)
            writefile.write(','.join(row))
            writefile.write('\n')

# Save an image of the embedding

def saveSignal(bORw, embeddingType, numLines, data):
    plt.plot(list(range(numLines)),data)
    plt.savefig('Pictures/' + bORw + '_embedding_' + embeddingType + '.png')
    plt.clf()

# list all ements in directory

def getFileNames(d):
    filesindir = []
    for elem in os.listdir(d):
        if os.path.isdir(elem):
            directory = []
            for el in os.listdir(elem):
                if os.path.isdir(el):
                    subdir = []
                    for e in os.listdir(el):
                        subdir.append(e)
                    directory.append(subdir)
                else:
                    directory.append(el)
            filesindir.append(directory)
        else:
            filesindir.append(elem)
    return filesindir

def persistenceDistance(filesindir, bORw):
    count = len(filesindir)**2
    if bORw == 'bottleneck':
        hera = './hera/geom_bottleneck/build/bottleneck_dist '
    else:
        hera = './hera/geom_matching/wasserstein/wasserstein_dist '
    with open('Data/' + bORw + '_values.csv', 'w') as file:
        file.write('file1,file2,'+ bORw + '_distance\n')
        for i in range(len(filesindir)):
            for j in range(i+1,len(filesindir)):
                #print(str(count) + ' ' + bORw + ' iterations left')
                count -= 1
                command_1 = 'echo ' + filesindir[i][20:-4] + ',' + filesindir[j][20:-4]
                command_2 = hera + './Data/persistence/persistence_diagram_' + filesindir[i][20:-4] + '.txt ./Data/persistence/persistence_diagram_' + filesindir[j][20:-4] + '.txt'
                echostream = os.popen(command_1)
                herastream = os.popen(command_2)
                file.write(echostream.read()[:-1] + ',' + herastream.read()[:-1] + '\n')

####################################################################################################
#                                                                                                  #
#                                    Non-Metric Functions                                          #
#                                                                                                  #
####################################################################################################

# Convert Euclidean to non-metric distance given a certain k

def non_met_distance(x, y, x_k, y_k):
    numer = distance(x,y)
    denom = max([x_k,y_k])
    return numer/denom

# sort the rows metric dissimilarity matrix by row

def sort_metric(mat, sorted_matrix):

    for i in range(0, len(mat[0])):
        sorted_row = np.sort(mat[i])
        sorted_matrix.append(sorted_row)

# map the metric dissimilarity matrix to a non-metric space

def metric_to_nonmetric(data, mat, sorted_matrix, k):
    nonmetric_dissimilarities = []
    
    for i in range(0, len(mat[0])):
        current_line = []

        for j in range(0, len(mat[0])):
            current_line.append(non_met_distance(data[i], data[j], sorted_matrix[i][k+1], sorted_matrix[j][k+1]))
        
        nonmetric_dissimilarities.append(current_line)
    
    return np.asanyarray(nonmetric_dissimilarities)

# map normal circle points to dense-to-sparse circle points

def dense_angle_to_sparse(angle,range_param):
    angle = angle % 2*pi
    if angle < 0:
        angle = angle + 2*pi
    
    vals = {
        0: [0,range_param],
        1: [range_param,2*pi-range_param],
        2: [2*pi-range_param,2*pi]
    }

    if angle < pi/2:
        alpha = 2*angle/pi
        min = vals[0][0]
        max = vals[0][1]
    elif angle >= pi/2 and angle <= 3*pi/2:
        alpha = (angle-(pi/2))/(pi)
        min = vals[1][0]
        max = vals[1][1]
    else:
        alpha = 2*(angle-(3*pi/2))/pi
        min = vals[2][0]
        max = vals[2][1]
    
    return min*(1-alpha) + max*alpha

