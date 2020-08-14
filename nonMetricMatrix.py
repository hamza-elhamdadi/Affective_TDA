from ripser import ripser
import math, nmf, geom, numpy as np, os, re, itertools

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
def floatify(arr):
    return list(map(lambda e: float(e), arr))

# get data from a file
def getData(filename, sects):
    with open(filename, 'r') as file:
        lines = file.readlines()

    temp = [
        floatify(line.split(' ')[1:]) 
        for line in lines
    ]

    extents = [{'section':s, 'indices':min_max(s)} for s in sects]

    return [{'section':e['section'], 'datapoints':temp[e['indices'][0]:e['indices'][1]]} for e in extents]

# make array nonmetric
def nonmetrify(metric_data):
    nonmetric_data = []
    for subsection in metric_data:
        curr = subsection['datapoints']  
        if subsection['section'] in ['leftEyebrow', 'rightEyebrow', 'leftEye', 'rightEye', 'innermouth', 'outermouth']:
            for i in range(len(curr)):
                edge = {
                    'section':subsection['section'],
                    'neighbors':[curr[i], curr[(i+1)%len(curr)]]
                }
                nonmetric_data.append(edge)
        else:
            for i in range(len(curr)-1):
                edge = {
                    'section':subsection['section'],
                    'neighbors':[curr[i], curr[i+1]]
                }
                nonmetric_data.append(edge)

    return nonmetric_data

# creates the nonmetric dissimilarity matrix for the data at filename
def getDissMatrix(filename, sects):
    metric_data = getData(filename, sects)

    nonmetric_data = nonmetrify(metric_data)

    ran = range(len(nonmetric_data))

    mat = []

    for i in ran:
        line = []
        for j in ran:
            temp = geom.segmentSegmentDistance(nonmetric_data[i].get('neighbors')[0],nonmetric_data[i].get('neighbors')[1],nonmetric_data[j].get('neighbors')[0],nonmetric_data[j].get('neighbors')[1])
            line.append(temp)
        mat.append(line)

    return mat


def build(f, s, dD):
    e = f.split('/')[-2]
    r = re.compile(r"\d{3}\.")

    num = f.split('/')[-1].split('.')[0]

    sects = '_'.join(s)
    outputPersistence1 = f'{dD}/subsections/persistence/h0/{sects}/persistence_diagram_{sects}_{e}_{num}.txt'
    outputPersistence2 = f'{dD}/subsections/persistence/h1/{sects}/persistence_diagram_{sects}_{e}_{num}.txt'

    mat = getDissMatrix(f, s)

    d = ripser(np.asarray(mat), distance_matrix=True)['dgms']
    d1 = d[0].tolist()
    d2 = d[1].tolist()

    for i in range(len(d1)):
        if d1[i][0] < math.pow(10,-8):
            d1[i][0] = float(0)
        if d1[i][1] < math.pow(10,-8):
            d1[i][1] = float(0)
    for i in range(len(d2)):
        if d2[i][0] < math.pow(10,-8):
            d2[i][0] = float(0)
        if d2[i][1] < math.pow(10,-8):
            d2[i][1] = float(0)

    with open(outputPersistence1, 'w') as file:
        for h in d1:
            if h[0] != h[1]:
                file.write(f'{h[0]} {h[1]}\n')

    with open(outputPersistence2, 'w') as file:
        for h in d2:
            if h[0] != h[1]:
                file.write(f'{h[0]} {h[1]}\n')

if __name__ == '__main__':
    dS = '../Data'
    dD = '../outputData/nonmetric/F001'

    files = nmf.getFileNames(dS, '.bnd')

    subsections = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'innermouth', 'outermouth', 'jawline']
    
    ret = []
    for i in range(1,len(subsections)+1):
        ret += itertools.combinations(subsections, i)
    ret = list(map(lambda l : list(l),ret))
    
    for filename in files:
        print(filename)
        for section_list in ret:
            build(filename, section_list, dD)