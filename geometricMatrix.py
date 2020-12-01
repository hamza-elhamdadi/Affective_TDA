from scipy.spatial import distance
import nmf, pandas as pd, itertools

emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise']
subsections = ['leftEye', 'rightEye', 'leftEyebrow', 'rightEyebrow', 'nose', 'mouth', 'jawline']

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

def read_bnd(filename, combination):
    values = list(pd.read_csv(filename, delimiter=' ', header=None, usecols=[1,2,3]).to_records(index=False))
    ret = []
    for section in combination:
        r = min_max(section)
        ret += values[r[0]:r[1]]
    return ret

def build_matrix(data):
    return [
        [
            sum([distance.euclidean(tuple(data[i][k]),tuple(data[j][k])) for k in range(len(data[i]))]) 
            for j in range(len(data))
        ] 
        for i in range(len(data))
    ]

if __name__ == '__main__':
    data_source = f'../Data/'
    data_destination = f'../outputData/geometry/F001/'
    
    files = nmf.getFileNames(data_source, '.bnd')

    combs = []
    for i in range(1,len(subsections)+1):
        combs += itertools.combinations(subsections, i)
    combs = list(map(lambda l : list(l),combs))

    for c in combs:
        for cc in c:
            print(c)
        out_file = '{}{}.csv'.format(data_destination, '_'.join(c))
        print(out_file)
        dissimilarities = build_matrix([
                read_bnd(f,c) 
                for f in files
            ])

        with open(out_file, 'w') as file:
            for line in dissimilarities:
                line = [str(l) for l in line]
                file.write('_'.join(line))

    






    #for f in files:
    #    print(f)