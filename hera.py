import os, nmf, multiprocessing as mp

def hera(f1, f2, oB, oW):
    b0 = os.popen('../hera/bottleneck/bottleneck_dist persistence_diagram_ {}'.format(f1)).read().split('\n')[:-1]
    b1 = os.popen('../hera/bottleneck/bottleneck_dist persistence_diagram_ {}'.format(f2)).read().split('\n')[:-1]

    b0 = list(map(lambda l: l.split(','), b0))
    b1 = list(map(lambda l: l.split(','), b1))

    b = []
    for j in range(len(b0)):
        p = b0[j][0]
        q = b0[j][1]
        r = str( sum( [ float(b0[j][2]), float(b1[j][2]) ] ) )
        b.append(','.join([p, q, r]))

    w0 = os.popen('../hera/wasserstein/wasserstein_dist persistence_diagram_ {}'.format(f1)).read().split('\n')[:-1]
    w1 = os.popen('../hera/wasserstein/wasserstein_dist persistence_diagram_ {}'.format(f2)).read().split('\n')[:-1]

    w0 = list(map(lambda l: l.split(','), w0))
    w1 = list(map(lambda l: l.split(','), w1))

    w = []
    for j in range(len(w0)):
        p = w0[j][0]
        q = w0[j][1]
        r = str(sum([float(w0[j][2]), float(w1[j][2])]))
        w.append(','.join([p, q, r]))

    with open(oB, 'w') as file:
        file.write('\n'.join(b))
    
    with open(oW, 'w') as file:
        file.write('\n'.join(w))

if __name__ == '__main__':
    filepath1 = '../outputData/nonmetric/F001/subsections/persistence/h0/'
    filepath2 = '../outputData/nonmetric/F001/subsections/persistence/h1/'

    files1 = []
    files2 = []

    for f in os.listdir(filepath1):
        if f.endswith('.txt'):
            files1.append(f'{filepath1}{f}')

    for f in os.listdir(filepath2):
        if f.endswith('.txt'):
            files2.append(f'{filepath2}{f}')

    dirs = list(map(lambda l: l[:l.find('_fileList')], map(lambda m: m.split('/')[-1], files1)))

    outFilesB = ['../outputData/nonmetric/F001/subsections/dissimilarities/bottleneck/{}.csv'.format(d) for d in dirs]
    outFilesW = ['../outputData/nonmetric/F001/subsections/dissimilarities/wasserstein/{}.csv'.format(d) for d in dirs]

    for i in range(len(files1)):
        hera(files1[i], files2[i], outFilesB[i], outFilesW[i])
        print(i)