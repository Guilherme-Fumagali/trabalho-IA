from random import random
import utils 
import statistics
from scipy.spatial import distance

def k_means(arq, k, iteracoes):
    label, datas = utils.readTableTxt(arq);
    clusters = []
    for i in range(0, k):
        while(True):
            obj = datas[int((len(datas) - 1) * random())];
            if obj not in clusters:
                clusters.append(obj)
                break

    clusters[0] = ["c1", 3.33, 116, 15]
    clusters[1] = ["c2", 7.33, 140, 27.33]
    clusters[2] = ["c3", 5, 176.66, 52]
    print(clusters)
    atualiza_clusters(dist(clusters, datas), clusters)

def dist(clusters, dados):
    res = []
    aux = []
    for d in dados:
        aux.append(d[0])
        for c in clusters:
            aux.append(distance.euclidean(d[1:], c[1:]))
        res.append(aux.copy()) 
        aux.clear() 
    return res

def atualiza_clusters(dados, clusters_antigos):
    clusters = []
    for i in clusters_antigos:
        clusters.append([])
    for d in dados:
        menor = min(d[1:])
        print(d.index(menor))
        clusters[d.index(menor)-1].insert(d.index(menor)-1, d)
    print(clusters)

    centroide = []
"""     
    centroide = clusters_antigos.copy()
    for c in centroide:
        for i in range(1, len(c)):
            c[i] = statistics.mean()

    print(centroide) 
"""



arq = open("/home/gfumagali/Documents/Trabalho IA/trabalho-IA/datasets/simpsons.txt");
k_means(arq, 3, 10);