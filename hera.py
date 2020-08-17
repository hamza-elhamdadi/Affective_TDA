import os, multiprocessing as mp
from random import randrange
import time

dim = 666
numCombs = {
        'm': 127,
        'nm': 255
    }

def hera(args):
    hb = '../hera/bottleneck/bottleneck_dist'
    hw = '../hera/wasserstein/wasserstein_dist'

    f1 = args.get('f1')
    f2 = args.get('f2')
    t = args.get('time')

    if f1 and f2:
        b0 = os.popen('{} {}'.format(hb, f1)).read().split('\n')[:-1]
        b1 = os.popen('{} {}'.format(hb, f2)).read().split('\n')[:-1]

        b0 = list(map(lambda l: l.split(' ')[:-1], b0))
        b1 = list(map(lambda l: l.split(' ')[:-1], b1))

        for j in range(dim):
            for k in range(dim):
                b0[j][k] = str(max(float(b0[j][k]), float(b1[j][k])))
            b0[j] = ' '.join(b0[j])  

        w0 = os.popen('{} {}'.format(hw, f1)).read().split('\n')[:-1]
        w1 = os.popen('{} {}'.format(hw, f2)).read().split('\n')[:-1]

        w0 = list(map(lambda l: l.split(' ')[:-1], w0))
        w1 = list(map(lambda l: l.split(' ')[:-1], w1))

        for j in range(dim):
            for k in range(dim):
                w0[j][k] = str(sum([float(w0[j][k]), float(w1[j][k])]))
            w0[j] = ' '.join(w0[j])

        with open(args.get('oB'), 'w') as file:
            file.write('\n'.join(b0))
        
        with open(args.get('oW'), 'w') as file:
            file.write('\n'.join(w0))
    elif f1:
        b = os.popen('{} {}'.format(hb, f1)).read()

        w = os.popen('{} {}'.format(hw, f1)).read()

        with open(args.get('oB'), 'w') as file:
            file.write(b)
    
        with open(args.get('oW'), 'w') as file:
            file.write(w)
    else:
        print('invalid args')

if __name__ == '__main__':
    metFilepath = '../outputData/metric/F001/subsections/metadata/'

    metFiles = []

    for f in os.listdir(metFilepath):
        metFiles.append(f'{metFilepath}{f}')

    mdirs = list(map(lambda l: l[:l.find('_fileList')], map(lambda m: m.split('/')[-1], metFiles)))

    moutFilesB = ['../outputData/metric/F001/subsections/dissimilarities/bottleneck/{}.csv'.format(d) for d in mdirs]
    moutFilesW = ['../outputData/metric/F001/subsections/dissimilarities/wasserstein/{}.csv'.format(d) for d in mdirs]

    ########################################################################################################################

    filepath1 = '../outputData/nonmetric/F001/subsections/metadata/h0/'
    filepath2 = '../outputData/nonmetric/F001/subsections/metadata/h1/'

    files1 = []
    files2 = []

    for f in os.listdir(filepath1):
        files1.append(f'{filepath1}{f}')

    for f in os.listdir(filepath2):
        files2.append(f'{filepath2}{f}')

    nmdirs = list(map(lambda l: l[:l.find('_fileList')], map(lambda m: m.split('/')[-1], files1)))

    nmoutFilesB = ['../outputData/nonmetric/F001/subsections/dissimilarities/bottleneck/{}.csv'.format(d) for d in nmdirs]
    nmoutFilesW = ['../outputData/nonmetric/F001/subsections/dissimilarities/wasserstein/{}.csv'.format(d) for d in nmdirs]

    for i in range(numCombs['m']):
        hera({'f1': metFiles[i], 'oB': moutFilesB[i], 'oW': moutFilesW[i]})
        print(f'metric {i}')
"""
    for i in range(numCombs['nm']):
        hera({'f1': files1[i], 'f2': files2[i], 'oB': nmoutFilesB[i], 'oW': nmoutFilesW[i]})
        print(f'nonmetric {i}')"""