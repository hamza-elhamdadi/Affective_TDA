from os import path
import re, os, nmf, time

emotions = ['_Angry', '_Disgust', '_Fear', '_Happy', '_Sad', '_Surprise']
subsections = ['leftEye_', 'rightEye_', 'leftEyebrow_','rightEyebrow_', 'nose_', 'mouth_', 'jawline_'] 

def hera(file1, file2, personID, path, subsection):
    filepaths = [
        'Data/' + personID + '/' + path + 'bottleneck/' + subsection + 'bottleneck_dissimilarities.csv', 
        'Data/' + personID + '/' + path + 'wasserstein/' + subsection + 'wasserstein_dissimilarities.csv'
    ]

    dists = [
        './hera/bottleneck/bottleneck_dist ', 
        './hera/wasserstein/wasserstein_dist '
    ]

    heras = [
        dist + file1 + ' ' + file2 
        for dist in dists
    ]

    lineparts = [
        filename[
            filename.find('persistence_diagram_')+len('persistence_diagram_') :
            filename.find('.')
        ] 
        for filename in [file1, file2]
    ]
    indices = ','.join(lineparts)
    streams = [os.popen(h) for h in heras]

    for i in range(2):
        csv_file = open(filepaths[i], 'a')
        csv_file.write(indices + ',' + streams[i].read()[:-1] + '\n')
    

dataSource = 'Data/F001/subsections/persistence/'
sources = list(map(lambda f : dataSource + f, os.listdir(dataSource)))
filesList = [nmf.getFileNames(d, '.txt') for d in sources]

if __name__ == '__main__':
    for filelist in filesList:
        for i in range(len(filelist)):
            for j in range(i+1, len(filelist)):
                hera(filelist[i],filelist[j], 'F001', 'subsections/dissimilarities/', filelist[i].split('/')[-2] + '_')