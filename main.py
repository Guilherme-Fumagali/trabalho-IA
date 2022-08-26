from random import random
from runpy import run_path
from sre_compile import isstring
import utils 
from scipy.spatial import distance

def k_means(arq, k, iteracoes):
    label, datas = utils.readTableTxt(arq);
    clusters = clusters_aleatorios(datas, k)

    for i in range(iteracoes):
        d = dist(clusters, datas)
        clusters = atualiza_centroides(datas, d, clusters)

    particao = []
    for c in clusters:
        particao.append(c[0])

    escrever_particao_no_arquivo("particao_kmedias.txt", particao)
    return particao

def single_link(arq, kMin, KMax):
    label, dados = utils.readTableTxt(arq)
    m_similaridade = matriz_similaridade(dados)
    particao = []
    for l in m_similaridade:
        particao.append(l[0])
    particoes = [particao]
    while(True):
        c = clusters_de_menor_dist(m_similaridade)
        m_similaridade = agrupa_single_link(m_similaridade, c[0], c[1])
        particao = []
        for l in m_similaridade:
            particao.append(l[0])
        particoes.append(particao)
        if(len(particao) == kMin):
            break
    
    particoes.reverse()
    return particoes[:KMax-kMin + 1]

def complete_link(arq, kMin, KMax):
    label, dados = utils.readTableTxt(arq)
    m_similaridade = matriz_similaridade(dados)
    particao = []
    for l in m_similaridade:
        particao.append(l[0])
    particoes = [particao]
    while(True):
        c = clusters_de_menor_dist(m_similaridade)
        m_similaridade = agrupa_complete_link(m_similaridade, c[0], c[1])
        particao = []
        for l in m_similaridade:
            particao.append(l[0])
        particoes.append(particao)
        if(len(particao) == kMin):
            break
    
    particoes.reverse()
    for i in particoes[:KMax-kMin + 1]:
        print(i)
    return particoes[:KMax-kMin + 1]

def matriz_similaridade(dados):
    matriz_similaridade = []
    
    for d in dados:
        distancias = dist([d], dados)
        linha = [[d[0]]]
        for i in range(len(distancias)):
            distancias[i] = remover_label(distancias[i])
        linha.append(utils.flat(distancias))
        matriz_similaridade.append(linha)
    return matriz_similaridade

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

def clusters_de_menor_dist(dados):
    menor = -1
    i_1_aux = -1
    i_2_aux = -1
    for d in dados:
        i_1_aux += 1
        for i in d[1]:
            i_2_aux += 1
            if(i != 0):
                if(menor == -1):
                    menor = i
                    i_1 = i_1_aux
                    i_2 = i_2_aux
                else:
                    if(i < menor):
                        menor = i
                        i_1 = i_1_aux
                        i_2 = i_2_aux
        i_2_aux = -1
                        
    return [i_1, i_2]

def agrupa_single_link(matriz_similaridade, i_1, i_2):
    linha_1 = matriz_similaridade[i_1]
    linha_2 = matriz_similaridade[i_2]

    labels = utils.flat([linha_1[0], linha_2[0]])

    matriz_similaridade.remove(linha_1)
    matriz_similaridade.remove(linha_2)

    for d in matriz_similaridade:
        d[1].pop(i_1)
        d[1].pop(i_2 - 1)

    dist = []
    for i in range(len(linha_1[1])):
        if(not (linha_1[1][i] == 0 or linha_2[1][i] == 0)):
            if(linha_1[1][i] < linha_2[1][i]):
                dist.append(linha_1[1][i])
            else:
                dist.append(linha_2[1][i])
    dist.insert(0, 0.0)
    
    i = 0
    for d in dist[1:]:
        matriz_similaridade[i][1].insert(0, d)
        i += 1


    linha = [labels, dist]
    matriz_similaridade.insert(0, linha)
    return matriz_similaridade

def agrupa_complete_link(matriz_similaridade, i_1, i_2):
    linha_1 = matriz_similaridade[i_1]
    linha_2 = matriz_similaridade[i_2]

    labels = utils.flat([linha_1[0], linha_2[0]])

    matriz_similaridade.remove(linha_1)
    matriz_similaridade.remove(linha_2)

    for d in matriz_similaridade:
        d[1].pop(i_1)
        d[1].pop(i_2 - 1)

    dist = []
    for i in range(len(linha_1[1])):
        if(not (linha_1[1][i] == 0 or linha_2[1][i] == 0)):
            if(linha_1[1][i] > linha_2[1][i]):
                dist.append(linha_1[1][i])
            else:
                dist.append(linha_2[1][i])
    dist.insert(0, 0.0)
    
    i = 0
    for d in dist[1:]:
        matriz_similaridade[i][1].insert(0, d)
        i += 1


    linha = [labels, dist]
    matriz_similaridade.insert(0, linha)
    return matriz_similaridade


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

def remover_label(dado):
    d = []
    for i in dado:
        if(not isstring(i)):
            d.append(i)
    return d


def escrever_particao_no_arquivo(caminho, particao):
    with open(caminho, "w") as arq:
        for cluster in particao:
            cluster.sort()
            print(cluster)
            for obj in cluster:
                arq.write("{:<10} {:<1}\n".format(obj, particao.index(cluster)))

arq = open("/home/gfumagali/Documents/Trabalho IA/trabalho-IA/datasets/simpsons.txt");
print(k_means(arq, 2, 10))