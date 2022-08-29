""" 
Grupo 01

Guilherme Fumagali Marques       - 792182 
Guilherme Silva de Camargo       - 792183
Rodrigo Henrique Amaral Araújo   - 792241 
Vinicius Gabriel Nanini da Silva - 795181

Arquivo principal, com a função main()
"""

import k_means
import utils
import single_complete_link
from sklearn.metrics.cluster import adjusted_rand_score

def main():
    #Dados necessários para a execução
    caminho_dados = "./datasets/monkey.txt"
    caminho_clusters_real = "./datasets/monkeyReal1.clu"
    KMin = 5 
    KMax = 12

    #Obtendo partição real
    dados_reais = utils.readTableTxt(open(caminho_clusters_real)) #lendo o arquivo e salvando em memória
    particao_real = []
    for d in dados_reais:
        particao_real.append(d[1] - 1) #vetor que armazena apenas os clusters dos objetos, em ordem
        
    #K-Médias
    print("K-médias")
    for k in range(KMin, KMax + 1): 
        dados_k_medias = k_means.k_means(open(caminho_dados), k, 7) #K-médias com 7 iterações e k clusters
        particao_k_medias = []
        for d in dados_k_medias:
            particao_k_medias.append(d[1]) #vetor que armazena apenas os clusters dos objetos, em ordem
        
        #AR da partição obtida, comparando-a com os dados reais
        print(f"k: {max(particao_k_medias) + 1} {adjusted_rand_score(particao_real, particao_k_medias)}")

    #Single-link
    dados_single_link = single_complete_link.single_link(open(caminho_dados), KMin, KMax) #Single-link com K-max - K-min partições
    print("Single-link")
    for d in dados_single_link: #para cada partição
        particao_single_link = []
        for p in d:
            particao_single_link.append(p[1]) #armazena apenas os clusters dos objetos, em ordem
        
        #AR da partição obtida, comparando-a com os dados reais
        print(f'k = {max(particao_single_link) + 1} {adjusted_rand_score(particao_real, particao_single_link)}')

    #Complete-link
    dados_complete_link = single_complete_link.complete_link(open(caminho_dados), KMin, KMax) #Complete-link com K-max - K-min partições
    print("Complete_link")
    for d in dados_complete_link: #para cada partição
        particao_complete_link = []
        for p in d:
            particao_complete_link.append(p[1]) #armazena apenas os clusters dos objetos, em ordem
        #AR da partição obtida, comparando-a com os dados reais
        print(f'k = {max(particao_complete_link) + 1} {adjusted_rand_score(particao_real, particao_complete_link)}')

main()

