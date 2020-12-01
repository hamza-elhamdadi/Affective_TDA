from ripser import ripser
from scipy.spatial import distance
import math, nmf, geom, numpy as np, os, re, itertools, time

nose_bridge_1 = 36
nose_bridge_2 = 47

cycle_sections = ['leftEyebrow', 'rightEyebrow', 'leftEye', 'rightEye', 'innermouth', 'outermouth']

# returns range of landmarks for a particular subsection
def min_max(subsection):
    return {
        "leftEye": (0,8),
        "rightEye": (8,16),                                                                                 
        "leftEyebrow": (16,26),
        "rightEyebrow": (26,36),
        "nose": (36,48),
        "innermouth": (48,60),
        "outermouth": (60,68),
        "jawline": (68,83)
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
        range_values = min_max(s)
        a = range_values[0]
        b = range_values[1]
        ret.append({'cyclical': s in cycle_sections, 'datapoints': data[a:b]})

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
    #nonmetric_data = make_nonmetric(metric_data['data'])

    data = []
    for i in range(len(metric_data['data'])):
        if metric_data['data'][i]['cyclical']:
            for j in range(len(metric_data['data'][i]['datapoints'])):
                data.append((metric_data['data'][i]['datapoints'][j], metric_data['data'][i]['datapoints'][(j+1)%len(metric_data['data'][i]['datapoints'])]))
        else:
            for j in range(len(metric_data['data'][i]['datapoints'])-1):
                data.append((metric_data['data'][i]['datapoints'][j], metric_data['data'][i]['datapoints'][(j+1)]))

    #print(data[0])

    mat = []
    for a in data:
        line = []
        for b in data:
            s0 = np.asarray(a[0])
            s1 = np.asarray(a[1])
            r0 = np.asarray(b[0])
            r1 = np.asarray(b[1])
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