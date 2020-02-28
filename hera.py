import multiprocessing
import nmf

filesindir = nmf.getFileNames('Data/persistence')

colors = ['cyan', 'yellow', 'red', 'green']

p_count = 2
process = []
bottleneck_data = multiprocessing.Manager().list()
wasserstein_data = multiprocessing.Manager().list()

for i in range( p_count ):
    process.append(multiprocessing.Process(target=nmf.persistenceDistance, args=(colors[i], bottleneck_data, filesindir, 'bottleneck', i, p_count)))
    process.append(multiprocessing.Process(target=nmf.persistenceDistance, args=(colors[i+2], wasserstein_data, filesindir, 'wasserstein', i, p_count ) ) )

for p in process:
    p.start()

for p in process:
    p.join()

with open('Data/bottleneck_dissimilarities.csv', 'w') as file:
    file.write('file1,file2,bottleneck_distance\n')
    for row in bottleneck_data:
        file.write(row[0]+ ',' + row[1] + ',' + row[2] + '\n')

with open('Data/wasserstein_dissimilarities.csv', 'w') as file:
    file.write('file1,file2,wasserstein_distance\n')
    for row in wasserstein_data:
        file.write(row[0]+ ',' + row[1] + ',' + row[2] + '\n')