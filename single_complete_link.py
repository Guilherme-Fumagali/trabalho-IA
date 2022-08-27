import utils
from sre_compile import isstring
from scipy.spatial import distance

def single_link(arq, kMin, KMax):
    dados = utils.readTableTxt(arq)
    m_similaridade = __matriz_similaridade(dados)
    particao = []
    for l in m_similaridade:
        particao.append(l[0])
    particoes = [particao]
    while(True):
        c = __clusters_de_menor_dist(m_similaridade)
        m_similaridade = agrupa_single_link(m_similaridade, c[0], c[1])
        particao = []
        for l in m_similaridade:
            particao.append(l[0])
        particoes.append(particao)
        if(len(particao) == kMin):
            break
    
    particoes.reverse()

    dados = []
    for particao in particoes[:KMax-kMin + 1]:
        dados.append(utils.escrever_particao_no_arquivo(f'single_link_k_{len(particao)}.txt', particao))
    
    return dados

def complete_link(arq, kMin, KMax):
    dados = utils.readTableTxt(arq)
    m_similaridade = __matriz_similaridade(dados)
    particao = []
    for l in m_similaridade:
        particao.append(l[0])
    particoes = [particao]
    while(True):
        c = __clusters_de_menor_dist(m_similaridade)
        m_similaridade = agrupa_complete_link(m_similaridade, c[0], c[1])
        particao = []
        for l in m_similaridade:
            particao.append(l[0])
        particoes.append(particao)
        if(len(particao) == kMin):
            break
    
    particoes.reverse()
    
    dados = []
    for particao in particoes[:KMax-kMin + 1]:
        dados.append(utils.escrever_particao_no_arquivo(f'single_link_k_{len(particao)}.txt', particao))
    
    return dados


def __matriz_similaridade(dados):
    matriz_similaridade = []
    
    for d in dados:
        distancias = __dist([d], dados)
        linha = [[d[0]]]
        for i in range(len(distancias)):
            distancias[i] = __remover_label(distancias[i])
        linha.append(utils.flat(distancias))
        matriz_similaridade.append(linha)
    return matriz_similaridade

def __clusters_de_menor_dist(dados):
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

def __remover_label(dado):
    d = []
    for i in dado:
        if(not isstring(i)):
            d.append(i)
    return d

def __dist(clusters, dados):
    res = []
    aux = []
    for d in dados:
        aux.append(d[0])
        for c in clusters:
            aux.append(distance.euclidean(d[1:], c[1:]))
        res.append(aux.copy()) 
        aux.clear() 
    return res