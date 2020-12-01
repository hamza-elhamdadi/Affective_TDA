import nmf, os

h0met = '../outputData/metric/M001/subsections/persistence/h0/'
h1met = '../outputData/metric/M001/subsections/persistence/h1/'
h0Dir = '../outputData/nonmetric/M001/subsections/persistence/h0/'
h1Dir = '../outputData/nonmetric/M001/subsections/persistence/h1/'


h0MetricOut = '../outputData/metric/M001/subsections/metadata/h0/'
h1MetricOut = '../outputData/metric/M001/subsections/metadata/h1/'
h0Out = '../outputData/nonmetric/M001/subsections/metadata/h0/'
h1Out = '../outputData/nonmetric/M001/subsections/metadata/h1/'

metricDirectories = os.listdir(h0met)
nonmetricDirectories = os.listdir(h0Dir)

def getFileNames(d, extension):                     
    files = []
    for f in os.listdir(d):
        files.append(f'{d}/{f}')
    return files

def contains2D(string):
    if not '2dimensional' in string:
        return True
    else:
        return False

metricH0 = [
    list(filter(
        lambda l: contains2D(l), 
        getFileNames(h0met + d, '.txt')
    ))
    for d in metricDirectories
]
metricH1 = [
    list(filter(
        lambda l: contains2D(l), 
        getFileNames(h1met + d, '.txt')
    ))
    for d in metricDirectories
]
filesH0 = [
    list(filter(
        lambda l: contains2D(l), 
        getFileNames(h0Dir + d, '.txt')
    ))
    for d in nonmetricDirectories
]
filesH1 = [
    list(filter(
        lambda l: contains2D(l), 
        getFileNames(h1Dir + d, '.txt')
    ))
    for d in nonmetricDirectories
]

for i in range(len(metricH0)):
    outputFileMetricH0 = f'{h0MetricOut}{metricDirectories[i]}_fileList.txt'
    outputFileMetricH1 = f'{h1MetricOut}{metricDirectories[i]}_fileList.txt'

    metricH0[i].sort()
    metricH1[i].sort()

    with open(outputFileMetricH0, 'w') as file:
        file.write('\n'.join(metricH0[i]))
        
    with open(outputFileMetricH1, 'w') as file:
        file.write('\n'.join(metricH1[i]))


for i in range(len(filesH0)):
    outputFileH0 = f'{h0Out}{nonmetricDirectories[i]}_fileList.txt'
    outputFileH1 = f'{h1Out}{nonmetricDirectories[i]}_fileList.txt'

    filesH0[i].sort()
    filesH1[i].sort()

    with open(outputFileH0, 'w') as file:
        file.write('\n'.join(filesH0[i]))

    with open(outputFileH1, 'w') as file:
        file.write('\n'.join(filesH1[i]))


