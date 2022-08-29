""" 
Grupo 01

Guilherme Fumagali Marques       - 792182 
Guilherme Silva de Camargo       - 792183
Rodrigo Henrique Amaral Araújo   - 792241 
Vinicius Gabriel Nanini da Silva - 795181

Arquivo com as funções que executam os algoritmos single-link e complete-link
"""

import utils
from sre_compile import isstring
from scipy.spatial import distance


""" 
Função principal, recebe um arquivo, KMin e KMax correspondente ao número de clusters desejados. E retorna
as partições desejadas.

OBS: o arquivo deve estar no formato .txt com os conjuntos de dados em que a primeira coluna representa um 
identificador dos objetos e as demais os atributos que devem ser considerados para o agrupamento.
"""
def single_link(arq, kMin, KMax):
    dados = utils.readTableTxt(arq) #Lendo o arquivo e salvando-o em memória
    m_similaridade = __matriz_similaridade(dados) #calculando a matriz de similaridade inicial
    particao = [] #vetor que armazenará a partição
    
    for l in m_similaridade:
        particao.append(l[0]) #adicionando os clusters a partição
    particoes = [particao] #partições armazena as partições de K clusters
    
    while(True):
        c = __clusters_de_menor_dist(m_similaridade) #encontra o par de clusters de menor distância
        m_similaridade = agrupa_single_link(m_similaridade, c[0], c[1]) #agrupa esse par de clusters
        particao = []
        for l in m_similaridade:
            particao.append(l[0]) #adicionando os clusters a partição
        particoes.append(particao) #Salvando essa partição
        if(len(particao) == kMin): #Se o K calculado for o Kmin, laço para.
            break
    
    particoes.reverse()

    dados = []
    for particao in particoes[:KMax-kMin + 1]: #escreve em disco as partições obtidas com K clusters desejados
        dados.append(utils.escrever_particao_no_arquivo(f'single_link_k_{len(particao)}.txt', particao))
    
    return dados #retorna os dados escritos em disco
    
""" 
Função principal, recebe um arquivo, KMin e KMax correspondente ao número de clusters desejados. E retorna
as partições desejadas.

OBS: o arquivo deve estar no formato .txt com os conjuntos de dados em que a primeira coluna representa um 
identificador dos objetos e as demais os atributos que devem ser considerados para o agrupamento.
"""
def complete_link(arq, kMin, KMax):
    dados = utils.readTableTxt(arq) #Lendo o arquivo e salvando-o em memória
    m_similaridade = __matriz_similaridade(dados) #calculando a matriz de similaridade inicial
    particao = [] #vetor que armazenará a partição
    
    for l in m_similaridade:
        particao.append(l[0]) #adicionando os clusters a partição
    particoes = [particao] #partições armazena as partições de K clusters
    
    while(True):
        c = __clusters_de_menor_dist(m_similaridade) #encontra o par de clusters de menor distância
        m_similaridade = agrupa_complete_link(m_similaridade, c[0], c[1]) #agrupa esse par de clusters
        particao = []
        for l in m_similaridade:
            particao.append(l[0]) #adicionando os clusters a partição
        particoes.append(particao) #Salvando essa partição
        if(len(particao) == kMin): #Se o K calculado for o Kmin, laço para.
            break
    
    particoes.reverse()
    
    dados = []
    for particao in particoes[:KMax-kMin + 1]: #escreve em disco as partições obtidas com K clusters desejados
        dados.append(utils.escrever_particao_no_arquivo(f'complete_link_k_{len(particao)}.txt', particao))
    
    return dados #retorna os dados escritos em disco


""" 
Função auxiliar a single_link() e complete_link().

Recebe os dados e retorna a matriz de similaridade.
"""
def __matriz_similaridade(dados):
    matriz_similaridade = []
    
    for d in dados: #Para cada dado na matriz
        distancias = __dist([d], dados) #Calcula a distância entre o objeto e os outros objetos
        linha = [[d[0]]] #Adiciona o identificador na linha
        for i in range(len(distancias)):
            distancias[i] = __remover_label(distancias[i])
        linha.append(utils.flat(distancias)) #adiciona a distância do objeto a outros objetos na linha
        matriz_similaridade.append(linha) #adiciona a linha a matriz
    return matriz_similaridade

""" 
Função auxiliar a single_link() e complete_link().

Recebe a matriz de similaridade e retorna os objetos mais próximos.
"""
def __clusters_de_menor_dist(dados):
    menor = -1
    i_1_aux = -1
    i_2_aux = -1
    for d in dados: #Busca sequencial pelo menor número na matriz
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
                        
    return [i_1, i_2] #retorna os índices do par de objeto mais próximo

""" 
Função auxiliar a single_link().

Recebe a matriz de similaridade e os índices dos pares mais próximos e os agrupa.
"""
def agrupa_single_link(matriz_similaridade, i_1, i_2):
    linha_1 = matriz_similaridade[i_1]
    linha_2 = matriz_similaridade[i_2]

    labels = utils.flat([linha_1[0], linha_2[0]]) #Une os identificadores

    matriz_similaridade.remove(linha_1) #Remove as linhas que serão agrupadas da matriz
    matriz_similaridade.remove(linha_2)

    for d in matriz_similaridade: #Em cada objeto remove as distâncias aos objetos que serão agrupados
        d[1].pop(i_1)
        d[1].pop(i_2 - 1)

    dist = []
    for i in range(len(linha_1[1])): #agrupa os objetos no critério do single-link
        if(not (linha_1[1][i] == 0 or linha_2[1][i] == 0)):
            if(linha_1[1][i] < linha_2[1][i]): #adiciona ao objeto a menor distância entre os outros clusters
                dist.append(linha_1[1][i])
            else:
                dist.append(linha_2[1][i])
    dist.insert(0, 0.0) #a distância entre o objeto e ele mesmo é zero
    
    i = 0
    for d in dist[1:]: #insere em todos os objetos a distância até esse nova linha agrupada
        matriz_similaridade[i][1].insert(0, d)
        i += 1

    linha = [labels, dist]
    matriz_similaridade.insert(0, linha) #insere essa linha em primeira posição da matriz
    return matriz_similaridade

""" 
Função auxiliar a complete_link().

Recebe a matriz de similaridade e os índices dos pares mais próximos e os agrupa.
"""
def agrupa_complete_link(matriz_similaridade, i_1, i_2):
    linha_1 = matriz_similaridade[i_1]
    linha_2 = matriz_similaridade[i_2]

    labels = utils.flat([linha_1[0], linha_2[0]]) #Une os identificadores

    matriz_similaridade.remove(linha_1) #Remove as linhas que serão agrupadas da matriz
    matriz_similaridade.remove(linha_2)

    for d in matriz_similaridade: #Em cada objeto remove as distâncias aos objetos que serão agrupados
        d[1].pop(i_1)
        d[1].pop(i_2 - 1)

    dist = []
    for i in range(len(linha_1[1])): #agrupa os objetos no critério do complete-link
        if(not (linha_1[1][i] == 0 or linha_2[1][i] == 0)): #adiciona ao objeto a maior distância entre os outros clusters
            if(linha_1[1][i] > linha_2[1][i]):
                dist.append(linha_1[1][i])
            else:
                dist.append(linha_2[1][i])
    dist.insert(0, 0.0) #a distância entre o objeto e ele mesmo é zero
    
    i = 0
    for d in dist[1:]: #insere em todos os objetos a distância até esse nova linha agrupada
        matriz_similaridade[i][1].insert(0, d)
        i += 1


    linha = [labels, dist]
    matriz_similaridade.insert(0, linha) #insere essa linha em primeira posição da matriz
    return matriz_similaridade

""" Remove as strings do objeto """
def __remover_label(dado):
    d = []
    for i in dado:
        if(not isstring(i)):
            d.append(i)
    return d

""" 
Função auxiliar a single_link() e complete_link().

Recebe os dados e clusters e retorna as distâncias entre eles.
"""
def __dist(clusters, dados):
    res = []
    aux = [] #aux é uma linha que vai pertencer a matriz de resultado
    for d in dados:
        aux.append(d[0]) #aux[0] é o identificador do objeto
        for c in clusters:
            aux.append(distance.euclidean(d[1:], c[1:])) #Linhas seguintes é a distância entre o objeto e cada cluster
        res.append(aux.copy()) 
        aux.clear() 
    return res