from sklearn.manifold import MDS
import operator as op
import matplotlib.pyplot as plt
import numpy as np
import nmf

bottleneck_dissimilarity = []
wasserstein_dissimilarity = []

length_of_file = 3

with open('Data/bottleneck_values.csv','r') as file:
    next(iter(file))
    for i in range(length_of_file):
        row = []
        for j in range(length_of_file):
            row.append(0)
        bottleneck_dissimilarity.append(row)
    for line in file:
        vals = line.split(',')
        bottleneck_dissimilarity[int(vals[0])][int(vals[1])] = float(vals[2])
        bottleneck_dissimilarity[int(vals[1])][int(vals[0])] = float(vals[2])
    with open('Data/bottleneck_dissimilarities.txt', 'w') as writefile:
        for row in bottleneck_dissimilarity:
            row = map(lambda val: str(val), row)
            writefile.write(','.join(row))
            writefile.write('\n')

with open('Data/wasserstein_values.csv','r') as file:
    next(iter(file))
    for i in range(length_of_file):
        row = []
        for j in range(length_of_file):
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
            writefile.write('\n')

embedding = MDS(n_components=2,dissimilarity='precomputed')

data_1 = embedding.fit_transform(np.asmatrix(bottleneck_dissimilarity))
data_2 = embedding.fit_transform(np.asmatrix(wasserstein_dissimilarity))

plt.scatter(map(op.itemgetter(0),data_1),map(op.itemgetter(1),data_1))
plt.savefig('Pictures/bottleneck_embedding.png')
plt.clf()
plt.scatter(map(op.itemgetter(0),data_2),map(op.itemgetter(1),data_2))
plt.savefig('Pictures/wasserstein_embedding.png')
plt.clf()