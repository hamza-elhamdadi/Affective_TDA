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
    temps = []
    for i in range(dimension):
        temp = (p1[i]-p0[i])**2
        temps.append(temp)
    return math.sqrt(sum(temps))

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

def dissMatFromHeraOut(file_lines, length_of_file):
    dissimilarity = np.zeros(shape=(length_of_file,length_of_file))
    for vals in file_lines:
        dissimilarity[vals[0]][vals[1]] = vals[2]
        dissimilarity[vals[1]][vals[0]] = vals[2]
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
    if embeddingType == 'MDS':
        plt.ylim(-1,1)
    elif embeddingType == 'Isomap':
        plt.ylim(-0.00000001,0.00000001)
    plt.savefig('Pictures/Lined/' + bORw + '_embedding_' + embeddingType + '.png')
    plt.clf()

    plt.plot(list(range(numLines))[:112],data[:112], color='b')                                 # Blue = Angry
    plt.plot(list(range(numLines))[:108],data[112:220], color='g')                              # Green = Disgust
    plt.plot(list(range(numLines))[:111],data[220:331], color='r')                              # Red = Fear
    plt.plot(list(range(numLines))[:111],data[331:442], color='c')                              # Cyan = Happy
    plt.plot(list(range(numLines))[:114],data[442:556], color='m')                              # Magenta = Sad
    plt.plot(list(range(numLines))[:110],data[556:], color='k')                                 # Black = Surprised
    if embeddingType == 'MDS':
        plt.ylim(-1,1)
    elif embeddingType == 'Isomap':
        plt.ylim(-0.00000001,0.00000001)
    plt.savefig('Pictures/Stacked/' + bORw + '_embedding_' + embeddingType + '_Stacked.png')
    plt.clf()

    plt.plot(list(range(numLines))[:112],data[:112])
    if embeddingType == 'MDS':
        plt.ylim(-1,1)
    elif embeddingType == 'Isomap':
        plt.ylim(-0.00000001,0.00000001)
    plt.savefig('Pictures/' + bORw + '_embedding_' + embeddingType + '_Angry.png')
    plt.clf()
    plt.plot(list(range(numLines))[:108],data[112:220])
    if embeddingType == 'MDS':
        plt.ylim(-1,1)
    elif embeddingType == 'Isomap':
        plt.ylim(-0.00000001,0.00000001)
    plt.savefig('Pictures/' + bORw + '_embedding_' + embeddingType + '_Disgust.png')
    plt.clf()
    plt.plot(list(range(numLines))[:111],data[220:331])
    if embeddingType == 'MDS':
        plt.ylim(-1,1)
    elif embeddingType == 'Isomap':
        plt.ylim(-0.00000001,0.00000001)
    plt.savefig('Pictures/' + bORw + '_embedding_' + embeddingType + '_Fear.png')
    plt.clf()
    plt.plot(list(range(numLines))[:111],data[331:442])
    if embeddingType == 'MDS':
        plt.ylim(-1,1)
    elif embeddingType == 'Isomap':
        plt.ylim(-0.00000001,0.00000001)
    plt.savefig('Pictures/' + bORw + '_embedding_' + embeddingType + '_Happy.png')
    plt.clf()
    plt.plot(list(range(numLines))[:114],data[442:556])
    if embeddingType == 'MDS':
        plt.ylim(-1,1)
    elif embeddingType == 'Isomap':
        plt.ylim(-0.00000001,0.00000001)
    plt.savefig('Pictures/' + bORw + '_embedding_' + embeddingType + '_Sad.png')
    plt.clf()
    plt.plot(list(range(numLines))[:110],data[556:])
    if embeddingType == 'MDS':
        plt.ylim(-1,1)
    elif embeddingType == 'Isomap':
        plt.ylim(-0.00000001,0.00000001)
    plt.savefig('Pictures/' + bORw + '_embedding_' + embeddingType + '_Surprise.png')
    plt.clf()

# list all ements in directory

###############################
#            TODO             #
###############################

# Make this recursive
# Check file extensions

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

def persistenceDistance(colorFlag, data, filesindir, bORw, start, step):
    print(colorFlag)
    if bORw == 'bottleneck':
        hera = './hera/geom_bottleneck/build/bottleneck_dist '
    else:
        hera = './hera/geom_matching/wasserstein/wasserstein_dist '
    for i in range(start,len(filesindir),step):
        for j in range(i+1,len(filesindir)):
            if filesindir[i][20:-4] != '' and filesindir[j][20:-4] != '':
                row = [filesindir[i][20:-4], filesindir[j][20:-4]]
                command_2 = hera + './Data/persistence/persistence_diagram_' + filesindir[i][20:-4] + '.txt ./Data/persistence/persistence_diagram_' + filesindir[j][20:-4] + '.txt'
                herastream = os.popen(command_2)
                row.append(herastream.read()[:-1])
                data.append(row)
    

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

