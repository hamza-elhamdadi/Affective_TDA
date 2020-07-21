from ripser import ripser
import math, nmf, geom, numpy as np, os, re, itertools

actionUnitsKey = { 
    "leftEye": (0,7), 
    "rightEye": (8,15),                                                                                 
    "leftEyebrow": (16,25),
    "rightEyebrow": (26,35),
    "nose": (36,47),
    "innermouth": (48,59),
    "outermouth": (60,67),
    "jawline": (68,82)
}

# map every element in array to float of itself
def floatify(arr):
    return list(map(lambda e: float(e), arr))

# get data from a file
def getData(filename, key, sects, containsHeader):
    lines = open(filename, 'r').readlines()

    temp = [
        floatify(line.split(' ')[1:]) 
        for line in (lines[1:] if containsHeader else lines)
    ]

    extents = [{'section':s, 'indices':key.get(s)} for s in sects]

    return [{'section':e['section'], 'datapoints':temp[e['indices'][0]:e['indices'][1]+1]} for e in extents]

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
def getDissMatrix(filename, key, sects, containsHeader):
    metric_data = getData(filename, key, sects, containsHeader)

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


def build(f, s, dD, e):
    r = re.compile(r"\d{3}\.")

    obj = r.search(f)
    num = f[obj.start():obj.end()-1]

    sects = '_'.join(s)
    outputDissimilarity = f'{dD}/subsections/dissimilarities/matrix_{sects}_{e}_{num}.txt'
    outputPersistence1 = f'{dD}/subsections/persistence/h0/persistence_diagram_{sects}_{e}_{num}.txt'
    outputPersistence2 = f'{dD}/subsections/persistence/h1/persistence_diagram_{sects}_{e}_{num}.txt'

    getDissMatrix(f, actionUnitsKey, s, False)

    mat = getDissMatrix(f, actionUnitsKey, s, False)

    with open(outputDissimilarity, 'w') as file:
        for m in mat:
            file.write(f'{m}\n')

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

    subsections = list(actionUnitsKey.keys())
    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise'] 
    
    ret = []
    for i in range(1,len(subsections)+1):
        ret += itertools.combinations(subsections, i)
    ret = list(map(lambda l : list(l),ret))
    
    for filename in files:
        print(filename)
        for section_list in ret:
            for emotion in emotions:
                build(filename, section_list, dD, emotion)