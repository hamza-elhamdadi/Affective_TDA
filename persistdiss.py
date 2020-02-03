from ripser import ripser
from persim import plot_diagrams
import nmf

bottleneck_dissimilarity = []
wasserstein_dissimilarity = []

with open('Data/bottleneck_values.csv','r') as file:
    next(iter(file))
    for i in range(len(list(file))):
        #print('hello')
        row = []
        for j in range(len(list(file))):
            print('hello')
            row.append(['hello'])
        bottleneck_dissimilarity.append(row)
    print(bottleneck_dissimilarity)
    for line in file:
        vals = line.split(',')
        bottleneck_dissimilarity[int(vals[0])][int(vals[1])] = float(vals[2])
        bottleneck_dissimilarity[int(vals[1])][int(vals[0])] = float(vals[2])
    with open('Data/bottleneck_dissimilarities.txt', 'w') as writefile:
        for row in bottleneck_dissimilarity:
            row = map(lambda val: str(val), row)
            writefile.write(','.join(row))

with open('Data/wasserstein_values.csv','r') as file:
    next(iter(file))
    for i in range(len(list(file))):
        row = []
        for j in range(len(list(file))):
            row.append(0)
        wasserstein_dissimilarity.append(row)
    for line in file:
        vals = line.split(',')
        wasserstein_dissimilarity[int(vals[0])][int(vals[1])] = float(vals[2])
        wasserstein_dissimilarity[int(vals[1])][int(vals[0])] = float(vals[2])
    with open('Data/wasserstein_dissimilarities.txt', 'w') as writefile:
        for row in wasserstein_dissimilarity:
            row = map(lambda val: str(val), row)
            writefile.write(','.join(row))