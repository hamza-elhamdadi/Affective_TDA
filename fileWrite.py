import nmf, os

metricDir = '../outputData/metric/F001/subsections/persistence/'
h0Dir = '../outputData/nonmetric/F001/subsections/persistence/h0/'
h1Dir = '../outputData/nonmetric/F001/subsections/persistence/h1/'

metricOut = '../outputData/metric/F001/subsections/metadata/'
h0Out = '../outputData/nonmetric/F001/subsections/metadata/h0/'
h1Out = '../outputData/nonmetric/F001/subsections/metadata/h1/'

metricDirectories = os.listdir(metricDir)
nonmetricDirectories = os.listdir(h0Dir)

def getFileNames(d, extension):                     
    files = []
    for f in os.listdir(d):
        files.append(f'{d}/{f}')
    return files

filesMetric = [getFileNames(metricDir + d, '.txt') for d in metricDirectories]
filesH0 = [getFileNames(h0Dir + d, '.txt') for d in nonmetricDirectories]
filesH1 = [getFileNames(h1Dir + d, '.txt') for d in nonmetricDirectories]

for i in range(len(filesMetric)):
    outputFileMetric = f'{metricOut}{metricDirectories[i]}_fileList.txt'

    with open(outputFileMetric, 'w') as file:
        file.write('\n'.join(filesMetric[i]))

for i in range(len(filesH0)):
    outputFileH0 = f'{h0Out}{nonmetricDirectories[i]}_fileList.txt'
    outputFileH1 = f'{h1Out}{nonmetricDirectories[i]}_fileList.txt'

    with open(outputFileH0, 'w') as file:
        file.write('\n'.join(filesH0[i]))

    with open(outputFileH1, 'w') as file:
        file.write('\n'.join(filesH1[i]))


