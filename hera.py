import os, multiprocessing as mp
from random import randrange
import time

person = 'F001'

dim = 666
numCombs = {
        'm': 127,
        'nm': 255
    }

def hera(args):
    #hb = '../hera/bottleneck/bottleneck_dist'
    hw = '../hera/wasserstein/wasserstein_dist'

    f1 = args.get('f1')
    f2 = args.get('f2')
    t = args.get('time')

    if f1 and f2:
        #b0 = [
        #    l.split(' ')[:-1] 
        #    for l in os.popen('{} {}'.format(hb, f1)).read().split('\n')[:-1]
        #] 
        #b1 = [
        #    l.split(' ')[:-1] 
        #    for l in os.popen('{} {}'.format(hb, f2)).read().split('\n')[:-1]
        #] 
        w0 = [
            l.split(' ')[:-1] 
            for l in os.popen('{} {}'.format(hw, f1)).read().split('\n')[:-1]
        ]
        w1 = [
            l.split(' ')[:-1] 
            for l in os.popen('{} {}'.format(hw, f2)).read().split('\n')[:-1]
        ]

        for j in range(dim):
            for k in range(dim):
                #b0[j][k] = str(max(float(b0[j][k]), float(b1[j][k])))
                w0[j][k] = str(sum([float(w0[j][k]), float(w1[j][k])]))
            #b0[j] = ' '.join(b0[j]) 
            w0[j] = ' '.join(w0[j])

        #print(len(b0))
        #print(b0[-1])

        #with open(args.get('oB'), 'w') as file:
        #    file.write('\n'.join(b0))
        
        with open(args.get('oW'), 'w') as file:
            file.write('\n'.join(w0))
    else:
        print('invalid args')

if __name__ == '__main__':
    metric_filepath_h0 = f'../outputData/metric/{person}/subsections/metadata/h0/'
    metric_filepath_h1 = f'../outputData/metric/{person}/subsections/metadata/h1/'

    nonmetric_filepath_h0 = f'../outputData/nonmetric/{person}/subsections/metadata/h0/'
    nonmetric_filepath_h1 = f'../outputData/nonmetric/{person}/subsections/metadata/h1/'

    metric_files = {
        'h0': [f'{metric_filepath_h0}{f}' for f in os.listdir(metric_filepath_h0)],
        'h1': [f'{metric_filepath_h1}{f}' for f in os.listdir(metric_filepath_h1)]
    }

    nonmetric_files = {
        'h0': [f'{nonmetric_filepath_h0}{f}' for f in os.listdir(nonmetric_filepath_h0)],
        'h1': [f'{nonmetric_filepath_h1}{f}' for f in os.listdir(nonmetric_filepath_h1)]
    }

    metric_directories = [
        l[:l.find('_fileList')] 
        for l in [
            m.split('/')[-1] 
            for m in metric_files['h0']
        ]
    ]

    nonmetric_directories = [
        l[:l.find('_fileList')] 
        for l in [
            m.split('/')[-1] 
            for m in nonmetric_files['h0']
        ]
    ]

    metric_output_filepaths = {
        #'bottleneck': ['../outputData/metric/{}/subsections/dissimilarities/bottleneck/{}.csv'.format(person, d) for d in metric_directories],
        'wasserstein': ['../outputData/metric/{}/subsections/dissimilarities/wasserstein2/{}.csv'.format(person, d) for d in metric_directories]
    }

    nonmetric_output_filepaths = {
        #'bottleneck': ['../outputData/nonmetric/{}/subsections/dissimilarities/bottleneck/{}.csv'.format(person, d) for d in nonmetric_directories],
        'wasserstein': ['../outputData/nonmetric/{}/subsections/dissimilarities/wasserstein2/{}.csv'.format(person, d) for d in nonmetric_directories]
    }

    for i in range(96,numCombs['m']):
        hera(
            {
                'f1': metric_files['h0'][i], 
                'f2': metric_files['h1'][i], 
    #            'oB': metric_output_filepaths['bottleneck'][i], 
                'oW': metric_output_filepaths['wasserstein'][i]
            }
        )
        print(f'metric {i}')

    for i in range(numCombs['nm']):
        hera(
            {
                'f1': nonmetric_files['h0'][i], 
                'f2': nonmetric_files['h1'][i], 
    #            'oB': nonmetric_output_filepaths['bottleneck'][i], 
                'oW': nonmetric_output_filepaths['wasserstein'][i]
            }
        )
        print(f'nonmetric {i}')