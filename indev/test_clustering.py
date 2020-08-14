import getData, matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering, DBSCAN

dissimilarities = getData.get_embedding_data(['rightEye'], 'bottleneck', 'tsne', 'Angry', 'metric', 30, True)

agcluster = AgglomerativeClustering(linkage='average', n_clusters=10, affinity='precomputed')
#dbscanCluster = DBSCAN(eps=1, metric='precomputed')

agcluster.fit(dissimilarities)
#dbscanCluster.fit(dissimilarities)

print(agcluster.labels_)
#print(dbscanCluster.labels_)

for i in range(len(agcluster.labels_)-1):
    if agcluster.labels_[i] != agcluster.labels_[i+1] and [agcluster.labels_[i], agcluster.labels_[i+1]] in [[8,3],[3,8]]:
        print(f'[{agcluster.labels_[i]},{agcluster.labels_[i+1]}] -> [{i},{i+1}]')

