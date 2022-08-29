""" 
Grupo 01

Guilherme Fumagali Marques       - 792182 
Guilherme Silva de Camargo       - 792183
Rodrigo Henrique Amaral Araújo   - 792241 
Vinicius Gabriel Nanini da Silva - 795181

Arquivo com a função que executa o algoritmo k-médias
"""

import utils 
from random import random
from sre_compile import isstring
from scipy.spatial import distance

""" 
Função principal, recebe um arquivo, k correspondente ao número de clusters desejados e a quantidade de iterações
que o algoritmo irá executar.

OBS: o arquivo deve estar no formato .txt com os conjuntos de dados em que a primeira coluna representa um 
identificador dos objetos e as demais os atributos que devem ser considerados para o agrupamento.
"""
def k_means(arq, k, iteracoes):
    datas = utils.readTableTxt(arq) #Lendo o arquivo e salvando-o em memória
    clusters = __clusters_aleatorios(datas, k) #Obtendo os primeiros clusters

    for i in range(iteracoes):  
        d = __dist(clusters, datas) #Calcula as distâncias entre os objetos e centróides
        clusters = __atualiza_centroides(datas, d, k) #Obtém os novos centróides a partir da menor distância

    particao = []
    for c in clusters: #Monta a partição em memória
        particao.append(c[0]) 

    #Escreve em disco e retorna os dados que foram escritos
    return utils.escrever_particao_no_arquivo(f'k_medias_k_{len(particao)}.txt', particao)

""" 
Função auxiliar a k_means().

Obtém k objetos aleatóros em um conjunto de dados.
"""
def __clusters_aleatorios(dados, k):
    clusters = []
    for i in range(0, k):
        while(True):
            #obj recebe um dado em um índice aleatório de dados
            obj = dados[int((len(dados) - 1) * random())];
            if obj not in clusters: #Evita objetos iguais
                clusters.append(obj)
                break
    return clusters

""" 
Função auxiliar a k_means().

Recebe os dados e os clusters, e retorna uma matriz com as distâncias calculadas.
"""
def __dist(clusters, dados):
    res = []
    aux = [] #aux é uma linha que vai pertencer a matriz de resultado
    for d in dados:
        aux.append(d[0]) #aux[0] é o identificador do objeto
        for c in clusters: #Linhas seguintes é a distância entre o objeto e cada cluster
            aux.append(distance.euclidean(d[1:], c[1:]))
        res.append(aux.copy()) 
        aux.clear() 
    return res

""" 
Função auxiliar a k_means().

Recebe os dados, as distâncias, e a quantidade de clusters na partição.
Retorna os novos centróides.
"""
def __atualiza_centroides(dados, dist, k):
    clusters = []
    for i in range(k):
        clusters.append([]) #Um objeto vazio em clusters para cada cluster

    for d in dist: #Percorre os dados das distâncias
        i_d = dist.index(d) #índice do objeto nos dados da distância
        menor = min(d[1:]) #obtém o centróide mais próximo
        i_menor = d.index(menor) - 1 #obtém o índice desse centroide no objeto
        clusters[i_menor].append(dados[i_d]) #adiciona no cluster mais próximo esse objeto

    centroides = []
    for c in clusters:
        centroides.append(__centroide(c)) #obtém as coordenadas dos novos centróides
    return centroides

""" 
Função auxiliar a __atualiza_centroides().

Recebe o cluster com os objetos que o pertence, e retorna a média de todos os
pontos desse cluster.
"""
def __centroide(cluster):
    label = [] #irá armazenar o identificador de todos os objetos do cluster
    ctd = [label] #armazena os dados que serão retornados, iniciando com o identificador dos objetos
    for i in range(len(cluster[0])-1):
        ctd.append(0) #inicializa ctd com zeros

    for c in cluster: #para cada objeto no cluster
        for i in range(len(c)): #percorre o objeto
            if(isstring(c[i])): #Se for o identificador, adiciona em label
                label.append(c[i])
            else:
                ctd[i] += c[i]  #Senão, soma no seu respectivo eixo da coordenada
    for i in range(1, len(ctd)):
        ctd[i] = ctd[i] / len(cluster) #Faz a média nas coordenadas
    return ctd