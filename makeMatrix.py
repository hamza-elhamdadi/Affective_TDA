from ripser import ripser
from scipy.spatial import distance
import time
import nmf, math, numpy as np, os, itertools

def min_max(subsection):
    return {
        "leftEye": (0,8),
        "rightEye": (8,16),                                                                                 
        "leftEyebrow": (16,26),
        "rightEyebrow": (26,36),
        "nose": (36,48),
        "mouth": (48,68),
        "jawline": (68,83)
    }.get(subsection)

def calcDissimilarity(filename, section_list):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    norm = distance.euclidean(
        [float(l) for l in lines[36].split(' ')[1:]],
        [float(l) for l in lines[47].split(' ')[1:]]
    )
    temp = list(map(lambda line: list(map(lambda l: float(l), line.split(' ')[1:])), lines))

    extent = [min_max(subsection) for subsection in section_list]
    data = [t for e in extent for t in temp[e[0]:e[1]]]

    mat = [[distance.euclidean(d[:-1], e[:-1])/norm for d in data] for e in data]          

    return np.asarray(mat)


def build(filename, section_list, dataDestination):
    diagrams = ripser(calcDissimilarity(filename, section_list), distance_matrix=True)['dgms']

    filepathH0 = '{}/persistence/h0/{}/persistence_diagram_{}_{}_{}.txt'.format(
        dataDestination, 
        '_'.join(section_list),
        '_'.join(section_list), 
        filename.split('/')[-2], 
        filename.split('/')[-1].split('.')[0]
    )
    filepathH1 = '{}/persistence/h1/{}/persistence_diagram_{}_{}_{}.txt'.format(
        dataDestination, 
        '_'.join(section_list),
        '_'.join(section_list), 
        filename.split('/')[-2], 
        filename.split('/')[-1].split('.')[0]
    )

    with open(filepathH0, 'w') as file:
        for feature in diagrams[0]:
            file.write(' '.join([str(f) for f in feature]))
            file.write('\n')

    with open(filepathH1, 'w') as file:
        for feature in diagrams[1]:
            file.write(' '.join([str(f) for f in feature]))
            file.write('\n')

if __name__ == '__main__':
    start = time.time()
    dS = '../Data/M001'
    dD = '../performanceData/metric/M001'

    files = nmf.getFileNames(dS, '.bnd')

    subsections = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'mouth', 'jawline']

    ret = [
        ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'mouth', 'jawline'],
        ['leftEye', 'rightEye', 'nose'],
        ['nose', 'mouth'],
        ['leftEyebrow', 'rightEyebrow', 'nose'],
    ]
    #ret = []
    #for i in range(1,len(subsections)+1):
    #    ret += itertools.combinations(subsections, i)
    #ret = list(map(lambda l : list(l),ret))

    for filename in files:
        for section_list in ret:
            build(filename, section_list, dD)

    print("--- %s seconds ---" % (time.time() - start))