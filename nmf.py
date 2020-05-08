# functions for the nonmetric_data_sets project

import math, re, numpy as np, matplotlib.pyplot as plt, os

pi = np.pi

pattern3 = re.compile(r"[a-zA-Z0-9]{4,12}_[a-zA-Z0-9]{3,8}_\d{3}\.")

extensionPattern = re.compile(r"\.[a-z]{3,5}$")

####################################################################################################
#                                                                                                  #
#                                        General Functions                                         #
#                                                                                                  #
####################################################################################################

# Euclidean distance between two points (supports two and three dimensions)

def distance(p0, p1, dimension):
    return math.sqrt(sum([(p1[i]-p0[i])**2 for i in range(dimension)]))      # return the Euclidean distance between the two points

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

# get frame number from file path string

def get_frame_number(string):
    if pat1:
        val = pattern3.search(string)
        if val == None:
            return None
        start = val.start()
        end = val.end()
        substring = string[start+1:end-1]

    return substring.split('_')

# list all elements in directory

def getFileNames(d, extension):                                     
    filesindir = []                                                     # empty list to add elements to
    for elem in os.listdir(d):                                          # for every element in the current path
        if os.path.isdir(d + '/' + elem):                               # check if the current path element is a directory
            filesindir += getFileNames(d + '/' + elem, extension)       # recursively call getFileNames on the current directory 
                                                                        # and add the results to the filesindir variable

        else:                                                           # otherwise the current path element is a file
            if elem[elem.find('.'):] == extension:                      # check if the file has the correct extension
                filesindir.append(d + '/' + elem)                       # append the current element with the filepath to the list
    return filesindir                                                   # return the list containing all filenames in current dir
    

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

