from os import path
import re, os, nmf, time

emotionFramePattern = re.compile(r"[a-zA-Z0-9]{4,12}_[a-zA-Z0-9]{3,8}_\d{3}\.")

def hera(file1, file2, personID, path, subsection):
    filepaths = ['Data/' + personID + '/' + path + subsection + 'bottleneck_dissimilarities.csv', 'Data/' + personID + '/' + path + subsection + 'wasserstein_dissimilarities.csv']

    dists = ['./hera/geom_bottleneck/build/bottleneck_dist ', './hera/geom_matching/wasserstein/wasserstein_dist ']
    heras = [dist + file1 + ' ' + file2 for dist in dists]

    lineparts = [emotionFramePattern.search(filename).group()[:-1] for filename in [file1, file2]]
    indices = ','.join(lineparts)
    streams = [os.popen(h) for h in heras]

    for i in range(2):
        csv_file = open(filepaths[i], 'a')
        csv_file.write(indices + ',' + streams[i].read()[:-1] + '\n')
    

subsections = ['leftEyebrow_','rightEyebrow_', 'nose_', 'mouth_']

dataSource = './Data/F001/subsections/persistence'

filesindir = nmf.getFileNames(dataSource, '.txt')

if __name__ == '__main__':
    for i in range(len(filesindir)):
        for j in range(i+1, len(filesindir)):
            for subsection in subsections:
                if subsection in filesindir[i] and subsection in filesindir[j]:
                    hera(filesindir[i],filesindir[j], 'F001', 'subsections/', subsection)