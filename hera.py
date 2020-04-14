import multiprocessing
from os import path
import nmf

def hera(section_list):
    filesindir = nmf.getFileNames('Data/persistence')

    colors = ['cyan', 'yellow', 'red', 'green']

    p_count = 2
    
    addition = ''

    if len(section_list) == 0:
        section = ''
    else:
        section = 'subsections/'

    for subsection in section_list:
        addition += subsection + '_'

    addition = section + addition

    bottleneck_filepath = 'Data/F001/' + addition + 'bottleneck_dissimilarities.csv'
    wasserstein_filepath = 'Data/F001/' + addition + 'wasserstein_dissimilarities.csv'

    bexists = path.exists(bottleneck_filepath)
    wexists = path.exists(wasserstein_filepath)

    process = []
    bottleneck_data = multiprocessing.Manager().list()
    wasserstein_data = multiprocessing.Manager().list()

    for i in range( p_count ):
        if not bexists:
            process.append(multiprocessing.Process(target=nmf.persistenceDistance, args=(addition, colors[i], bottleneck_data, filesindir, 'bottleneck', i, p_count)))
        if not wexists:
            process.append(multiprocessing.Process(target=nmf.persistenceDistance, args=(addition, colors[i+2], wasserstein_data, filesindir, 'wasserstein', i, p_count ) ) )

    for p in process:
        p.start()

    for p in process:
        p.join()

    if not bexists:
        with open(bottleneck_filepath, 'w') as file:
            file.write('file1,file2,bottleneck_distance\n')
            for row in bottleneck_data:
                file.write(row[0]+ ',' + row[1] + ',' + row[2] + '\n')

    if not wexists:                         
        with open(wasserstein_filepath, 'w') as file:
            file.write('file1,file2,wasserstein_distance\n')
            for row in wasserstein_data:
                file.write(row[0]+ ',' + row[1] + ',' + row[2] + '\n')

if __name__ == '__main__':
    hera()