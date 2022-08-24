from random import random
from sre_compile import isstring
import utils 
from scipy.spatial import distance

def k_means(arq, k, iteracoes):
    label, datas = utils.readTableTxt(arq);
    clusters = clusters_aleatorios(datas, k)

    for i in range(iteracoes):
        d = dist(clusters, datas)
        clusters = atualiza_centroides(datas, d, clusters)


    dados_separados = []
    i = 0
    for c in clusters:
        for label in c[0]:
            dados_separados.append([label, i])
        i += 1

    for i in dados_separados:
        print(i)    
    return dados_separados

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

def clusters_aleatorios(dados, k):
    clusters = []
    for i in range(0, k):
            while(True):
                obj = dados[int((len(dados) - 1) * random())];
                if obj not in clusters:
                    clusters.append(obj)
                    break
    return clusters

def atualiza_centroides(dados, dist,clusters_antigos):
    clusters = []
    
    for i in clusters_antigos:
        clusters.append([])

    for d in dist:
        i_d = dist.index(d)
        menor = min(d[1:])
        i_menor = d.index(menor) - 1
        clusters[i_menor].append(dados[i_d])

    centroides = []
    for c in clusters:
        centroides.append(centroide(c))
    return centroides


def centroide(cluster):
    label = []
    ctd = [label]
    for i in range(len(cluster[0])-1):
        ctd.append(0)
    for c in cluster:
        for i in range(len(c)):
            if(isstring(c[i])):
                label.append(c[i])
            else:
                ctd[i] += c[i] 
    for i in range(1, len(ctd)):
        ctd[i] = ctd[i] / len(cluster)
    return ctd


arq = open("/home/gfumagali/Documents/Trabalho IA/trabalho-IA/datasets/c2ds1-2sp.txt");
k_means(arq, 2, 10);