from ripser import ripser
from scipy.spatial import distance
import math, nmf, geom, numpy as np, os, re, itertools, time

nose_bridge_1 = 36
nose_bridge_2 = 47

cycle_sections = ['leftEyebrow', 'rightEyebrow', 'leftEye', 'rightEye', 'innermouth', 'outermouth']

# returns range of landmarks for a particular subsection
def min_max(subsection):
    return {
        "leftEye": [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0)],
        "rightEye": [(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,0)],                                                                                 
        "leftEyebrow": [(16,17),(17,18),(18,19),(19,20),(20,21),(21,22),(22,23),(23,24),(24,25),(25,0)],
        "rightEyebrow": [(26,27),(27,28),(28,29),(29,30),(30,31),(31,32),(32,33),(33,34),(34,35),(35,0)],
        "nose": [(36,37),(37,38),(38,39),(39,40),(40,41),(41,42),(42,43),(43,44),(44,45),(45,46),(46,47)],
        "innermouth": [(48,49),(49,50),(50,51),(51,52),(52,53),(53,54),(54,55),(55,56),(56,57),(57,58),(58,59),(59,0)],
        "outermouth": [(60,61),(61,62),(62,63),(63,64),(64,65),(65,66),(66,67),(67,0)],
        "jawline": [(67,68),(69,70),(70,71),(71,72),(72,73),(73,74),(74,75),(75,76),(76,77),(77,78),(78,79),(79,80),(80,81),(81,82)]
    }.get(subsection)

# map every element in array to float of itself
def floatify(line):
    return [float(e) for e in line.split(' ')[1:]]

# length for cycle conditionals
def len_conditional(curr, is_cycle):
    return len(curr) if is_cycle else len(curr)-1

# index for cycle conditionals
def index_conditional(curr, i, is_cycle):
    return (i+1)%len(curr) if is_cycle else i+1

#returns a data object representing the subsections of the face
# (calls min_max)
def get_data_object(data, sects):
    ret = []
    for s in sects:
        edges = min_max(s)
        for e in edges:
            ret.append(np.asarray((data[e[0]],data[e[1]])))

    return ret

# get data from a file
# (calls floatify and get_data_object)
def parse_file(filename, sects):
    with open(filename, 'r') as file:
        data = [floatify(line) for line in file.readlines()]

    return {
        'data': get_data_object(data, sects),
        'norm': distance.euclidean(data[nose_bridge_1], data[nose_bridge_2])
    }

# make array nonmetric 
# (calls make_edge)
#def make_nonmetric(metric_data):
#
#    nonmetric_data = []
#    for subsection in metric_data:
#        r = len_conditional(subsection['datapoints'], subsection['cyclical'])
#        for i in range(r):
#            j = index_conditional(subsection['datapoints'],i, subsection['cyclical'])
#            nonmetric_data.append({
#                    'neighbors': [
#                        subsection['datapoints'][i], 
#                        subsection['datapoints'][j]
#                    ]
#                })
#
#    return nonmetric_data

# creates the nonmetric dissimilarity matrix for the data at filename
def get_dissimilarity_matrix(filename, sects):
    metric_data = parse_file(filename, sects)
    data = metric_data['data']
    #nonmetric_data = make_nonmetric(metric_data['data'])

    #data = []
    #for i in range(len(metric_data['data'])):
    #    if metric_data['data'][i]['cyclical']:
    #        for j in range(len(metric_data['data'][i]['datapoints'])):
    #            data.append((np.asarray(metric_data['data'][i]['datapoints'][j]), np.asarray(metric_data['data'][i]['datapoints'][(j+1)%len(metric_data['data'][i]['datapoints'])])))
    #    else:
    #        for j in range(len(metric_data['data'][i]['datapoints'])-1):
    #            data.append((np.asarray(metric_data['data'][i]['datapoints'][j]), np.asarray(metric_data['data'][i]['datapoints'][(j+1)])))

    mat = []
    for a in data:
        line = []
        for b in data:
            s0 = a[0]
            s1 = a[1]
            r0 = b[0]
            r1 = b[1]
            line.append(geom.seg_seg_distance(s0,s1,r0,r1)/metric_data['norm'])
        mat.append(line)

    return mat


def build(f, s, dD):
    e = f.split('/')[-2]
    num = f.split('/')[-1].split('.')[0]

    sects = '_'.join(s)
    f1 = f'{dD}/persistence/h0/{sects}/persistence_diagram_{sects}_{e}_{num}.txt'
    f2 = f'{dD}/persistence/h1/{sects}/persistence_diagram_{sects}_{e}_{num}.txt'

    d = ripser(np.asarray(get_dissimilarity_matrix(f, s)), distance_matrix=True)['dgms']

    with open(f1, 'w') as file:
        for h in d[0].tolist():
            file.write(f'{h[0]} {h[1]}\n')

    with open(f2, 'w') as file:
        for h in d[1].tolist():
            file.write(f'{h[0]} {h[1]}\n')

if __name__ == '__main__':
    start = time.time()
    dS = '../Data/F001'
    dD = '../performanceData/nonmetric/F001'

    files = nmf.getFileNames(dS, '.bnd')

    subsections = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'innermouth', 'outermouth', 'jawline']
    
    ret = [
        ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'innermouth', 'outermouth', 'jawline'],
        ['leftEye', 'rightEye', 'nose'],
        ['nose', 'innermouth', 'outermouth'],
        ['leftEyebrow', 'rightEyebrow', 'nose']
    ]
    #ret = []
    #for i in range(1,len(subsections)+1):
    #    ret += itertools.combinations(subsections, i)
    #ret = list(map(lambda l : list(l),ret))
  
    for filename in files:
        for section_list in ret:
            build(filename, section_list, dD)

    print(time.time() - start)