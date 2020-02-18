from sklearn.manifold import MDS, TSNE, Isomap
import operator as op
import numpy as np
import nmf

length_of_file = 112
embeddings = ['MDS', 'TSNE', 'Isomap']

bottleneck_dissimilarities = nmf.dissMatFromHeraOut('Data/bottleneck_values.csv', length_of_file)
wasserstein_dissimilarities = nmf.dissMatFromHeraOut('Data/wasserstein_values.csv', length_of_file)
"""nmf.writeDissimilarityMatrix('Data/bottleneck_dissimilarities.txt', bottleneck_dissimilarities)"""
"""nmf.writeDissimilarityMatrix('Data/wasserstein_dissimilarities.txt', wasserstein_dissimilarities)"""

embedding_MDS = MDS(n_components=1,dissimilarity='precomputed')
embedding_TSNE = TSNE(n_components=1,metric='precomputed')
embedding_Isomap = Isomap(n_components=1,metric='precomputed')

data_1 = [embedding_MDS.fit_transform(np.asmatrix(bottleneck_dissimilarity)), 
          embedding_TSNE.fit_transform(np.asmatrix(bottleneck_dissimilarity)), 
          embedding_Isomap.fit_transform(np.asmatrix(bottleneck_dissimilarity))]

data_2 = [embedding_MDS.fit_transform(np.asmatrix(wasserstein_dissimilarity)), 
          embedding_TSNE.fit_transform(np.asmatrix(wasserstein_dissimilarity)), 
          embedding_Isomap.fit_transform(np.asmatrix(wasserstein_dissimilarity))]

for i in range(3):
    nmf.saveSignal('bottleneck', embeddings[i], length_of_file, data_1[i])
    nmf.saveSignal('wasserstein', embeddings[i], length_of_file, data_2[i])