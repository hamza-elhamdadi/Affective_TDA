# functions for the nonmetric_data_sets project

import math
import numpy as np

pi = np.pi

# Euclidean distance between two points

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

# Convert Euclidean to non-metric distance given a certain k

def non_met_distance(x, y, x_k, y_k):
    numer = distance(x,y)
    denom = max([x_k,y_k])
    return numer/denom

# create the metric dissimilarity matrix

def dissim_matrix(data):
    dissimilarities = []

    for i in range(0,len(data)):
        current_line = []

        for j in range(0,len(data)):
            current_line.append(distance(data[i],data[j]))
        
        dissimilarities.append(current_line)

    return np.asanyarray(dissimilarities)

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

# generate randomness values

def rand_vals(start, end, num_dp):
    return [np.random.uniform(start, end) for x in range(0,num_dp+1)]

