from sklearn.manifold import MDS, TSNE, Isomap
import operator as op
import matplotlib.pyplot as plt
import numpy as np
import nmf

length_of_file = 112

with open('Data/bottleneck_values.csv','r') as file:
    next(iter(file))
    bottleneck_dissimilarity = np.zeros(shape=(length_of_file,length_of_file))
    for line in file:
        vals = line.split(',')
        bottleneck_dissimilarity[int(vals[0])][int(vals[1])] = float(vals[2])
        bottleneck_dissimilarity[int(vals[1])][int(vals[0])] = float(vals[2])
    """with open('Data/bottleneck_dissimilarities.txt', 'w') as writefile:
        for row in bottleneck_dissimilarity:
            row = map(lambda val: str(val), row)
            writefile.write(','.join(row))
            writefile.write('\n')"""

with open('Data/wasserstein_values.csv','r') as file:
    next(iter(file))
    wasserstein_dissimilarity = np.zeros(shape=(length_of_file,length_of_file))
    for line in file:
        vals = line.split(',')
        wasserstein_dissimilarity[int(vals[0])][int(vals[1])] = float(vals[2])
        wasserstein_dissimilarity[int(vals[1])][int(vals[0])] = float(vals[2])
    """with open('Data/wasserstein_dissimilarities.txt', 'w') as writefile:
        for row in wasserstein_dissimilarity:
            row = map(lambda val: str(val), row)
            writefile.write(','.join(row))
            writefile.write('\n')"""

x_vals = list(range(length_of_file))

embedding_MDS = MDS(n_components=1,dissimilarity='precomputed')
embedding_TSNE = TSNE(n_components=1,metric='precomputed')
embedding_Isomap = Isomap(n_components=1,metric='precomputed')

MDS_data_1 = embedding_MDS.fit_transform(np.asmatrix(bottleneck_dissimilarity))
MDS_data_2 = embedding_MDS.fit_transform(np.asmatrix(wasserstein_dissimilarity))

TSNE_data_1 = embedding_TSNE.fit_transform(np.asmatrix(bottleneck_dissimilarity))
TSNE_data_2 = embedding_TSNE.fit_transform(np.asmatrix(wasserstein_dissimilarity))

Isomap_data_1 = embedding_Isomap.fit_transform(np.asmatrix(bottleneck_dissimilarity))
Isomap_data_2 = embedding_Isomap.fit_transform(np.asmatrix(wasserstein_dissimilarity))

# Bottleneck MDS
plt.plot(x_vals,MDS_data_1)
plt.savefig('Pictures/bottleneck_embedding_MDS.png')
plt.clf()
# Wasserstein MDS
plt.plot(x_vals,MDS_data_2)
plt.savefig('Pictures/wasserstein_embedding_MDS.png')
plt.clf()

# Bottleneck TSNE
plt.plot(x_vals,TSNE_data_1)
plt.savefig('Pictures/bottleneck_embedding_TSNE.png')
plt.clf()
# Wasserstein TSNE
plt.plot(x_vals,TSNE_data_2)
plt.savefig('Pictures/wasserstein_embedding_TSNE.png')
plt.clf()

# Bottleneck Isomap
plt.plot(x_vals,Isomap_data_1)
plt.savefig('Pictures/bottleneck_embedding_Isomap.png')
plt.clf()
# Wasserstein Isomap
plt.plot(x_vals,Isomap_data_2)
plt.savefig('Pictures/wasserstein_embedding_Isomap.png')
plt.clf()