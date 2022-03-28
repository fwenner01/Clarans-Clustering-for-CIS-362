from pyclustering.cluster.clarans import clarans
from pyclustering.cluster.silhouette import silhouette
import csv
import statistics

with open('live.csv', newline='') as f:
    reader = csv.DictReader(f)
    data = []
    for row in reader:
        data.append([int(row['num_reactions']), int(row['num_comments']), int(row['num_shares']), int(row['num_likes']), int(row['num_loves']), int(row['num_wows'])])

# Returns a dictionary with the clusters, the medoids, and the silouette score of the data
def claran_data(data, num_clusters, num_local, max_neighbor):
    d = dict();
    clarans_instance = clarans(data, num_clusters, num_local, max_neighbor)
    clarans_instance.process()
    d['clusters'] = clarans_instance.get_clusters()
    d['medoids'] = clarans_instance.get_medoids()
    score = silhouette(data, d['clusters']).process().get_score()
    score_sum = 0
    for i in score:
        score_sum += i
    d['score_average'] = score_sum / len(score)
    return d

# Returns a list with the median and standard deviation of cluster
# attributes: 0 - num_reactions, 1 - num_comments, 2 - num_shares, 3 - num_likes, 4 - num_loves, 5 - num_wows
def get_cluster_stats(data, cluster_data, attribute):
    l = []
    for i in cluster_data:
        l.append(data[i][attribute])
    return [statistics.median(l), statistics.pstdev(l)]
    
def print_stats(data, clusters, attribute):
    for i in range(len(clusters)):
        stats = get_cluster_stats(data, clusters[i], attribute)
        print("\nCluster ", (i + 1), ": Median - ", stats[0], " Standard Deviation - ", stats[1], "( attribute ", attribute, ")")
        


c = claran_data(data, 6, 4, 3)

print_stats(data, c['clusters'], 0)
print_stats(data, c['clusters'], 1)
print_stats(data, c['clusters'], 2)

print("\nThe index of medoids: ", c['medoids'])

print("\nSilhouette score: ", c['score_average'])
