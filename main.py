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

def single_link(arq, kMin, KMax):
    label, dados = utils.readTableTxt(arq)
    m_similaridade = matriz_similaridade(dados)
    c = clusters_de_menor_dist(m_similaridade)
    agrupa_single_link(m_similaridade, c[0], c[1])

def matriz_similaridade(dados):
    matriz_similaridade = []
    
    for d in dados:
        distancias = dist([d], dados)
        linha = [d[0]]
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
    i_1 = -1
    i_2 = -1
    for d in dados:
        for i in d[1]:
            if(i != 0):
                if(menor == -1):
                    menor = i
                else:
                    if(i < menor):
                        menor = i
                        i_1 = d.index(d[1])
                        i_2 = d[1].index(menor)
                        
    return [i_1, i_2]

"""         Homer Maggie Abe Selma
    Homer
    Maggie 
    Abe
    Selma

    Homer, Maggie

                    [Homer, Maggie] Abe Selma 
    [Homer, Maggie]
    Abe
    Selma
 """
def agrupa_single_link(matriz_similaridade, i_1, i_2):
    linha_1 = matriz_similaridade[i_1]
    linha_2 = matriz_similaridade[i_2]

    labels = [linha_1[0], linha_2[0]]

    m_similaridade_sem_labels = matriz_similaridade.copy()
    m_similaridade_sem_labels.remove(linha_1)
    m_similaridade_sem_labels.remove(linha_2)

    for d in m_similaridade_sem_labels:
        d[1].pop(i_1)
        d[1].pop(i_2-1)

    dist = []
    for i in range(len(linha_1[1])):
        if(not (linha_1[1][i] == 0 or linha_2[1][i] == 0)):
            if(linha_1[1][i] < linha_2[1][i]):
                dist.append(linha_1[1][i])
            else:
                dist.append(linha_2[1][i])
    linha = [labels, dist]
    """ Paramo aqui """
    """ falta colocar a posicao zero da linha como zero e inserir na matriz de similaridade """



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

arq = open("/home/gfumagali/Documents/Trabalho IA/trabalho-IA/datasets/simpsons.txt");
#k_means(arq, 2, 10);
single_link(arq, 0, 10);