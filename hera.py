from os import path
import re, os, nmf, time

hera_key = {
    'bottleneck':'./hera/bottleneck/bottleneck_dist', 
    'wasserstein':'./hera/wasserstein/wasserstein_dist'
}

def snip(string, begin, end):
    return string[string.find(begin)+len(begin):string.find(end)]

# boost package: sudo apt-get install libboost-all-dev

"""
format for inputs:
    {
        first: [h0 filepath, h1 filepath] or [filepath], <- type list of strings
        second: [h0 filepath, h1 filepath] or [filepath] <- type list of strings
    }

format for outputs:
    {
        bottleneck: filepath, <- type string
        wasserstein: filepath <- type string
    }

format for dists:
    {
        bottleneck: filepath <- type string,
        wasserstein: filepath <- type string
    }
"""

def hera(inputs, outputs, dists):
    f = inputs.get('first')
    s = inputs.get('second')
    b = dists.get('bottleneck')
    w = dists.get('wasserstein')
    p = 'persistence_diagram_'
    d = '.'

    streams = {
        'bottleneck': os.popen('{} {} {}'.format(b, f, s))
        'wasserstein': os.popen('{} {} {}'.format(w, f, s))
    }

    indices = '{},{}'.format(snip(f, p, d), snip(s, p, d))

    for met in list(streams.keys()):
        with open(outputs.get(met), 'a') as csv.file:
            csv_file.write('{},{}\n'.format(indices, streams.get(met).read()[:-1]))


dataSource = '../outputData/metric/F001/subsections/persistence/'
sources = list(map(lambda f : dataSource + f, os.listdir(dataSource)))
filesList = [nmf.getFileNames(d, '.txt') for d in sources]

#outputs = [
    #'../outputData/metric/' + personID + '/' + path + 'bottleneck/' + subsection + 'bottleneck_dissimilarities.csv', 
    # '../outputData/metric/' + personID + '/' + path + 'wasserstein/' + subsection + 'wasserstein_dissimilarities.csv'
#]

#dists = [
    #'./hera/bottleneck/bottleneck_dist ', 
    #'./hera/wasserstein/wasserstein_dist '
#]

"""if __name__ == '__main__':
    dataSource = '../outputData/metric/F001/subsections/persistence/'
    sources = list(map(lambda f : dataSource + f, os.listdir(dataSource)))
    filesList = [nmf.getFileNames(d, '.txt') for d in sources]

    for filelist in filesList:
        for i in range(len(filelist)):
            for j in range(i+1, len(filelist)):
                hera(filelist[i],filelist[j], 'F001', 'subsections/dissimilarities/', filelist[i].split('/')[-2] + '_')"""

