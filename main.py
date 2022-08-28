import k_means
import utils
import single_complete_link
from sklearn.metrics.cluster import adjusted_rand_score

def main():
    caminho_dados = "datasets\c2ds3-2g.txt"
    caminho_clusters_real = "datasets\c2ds3-2gReal.clu"
    KMin = 2 
    KMax = 5

    #Obtendo partição real
    dados_reais = utils.readTableTxt(open(caminho_clusters_real))
    particao_real = []
    for d in dados_reais:
        particao_real.append(d[1] - 1)
        
    #k-medias
    print("K-médias")
    for k in range(KMin, KMax + 1):
        dados_k_medias = k_means.k_means(open(caminho_dados), k, 7)
        particao_k_medias = []
        for d in dados_k_medias:
            particao_k_medias.append(d[1])
            
        print(f"k: {max(particao_k_medias) + 1} {adjusted_rand_score(particao_real, particao_k_medias)}")

    #Single-link
    dados_single_link = single_complete_link.single_link(open(caminho_dados), KMin, KMax)
    print("Single-link")
    for d in dados_single_link:
        particao_single_link = []
        for p in d:
            particao_single_link.append(p[1])
        print(f'k = {max(particao_single_link) + 1} {adjusted_rand_score(particao_real, particao_single_link)}')

    #Complete-link
    dados_complete_link = single_complete_link.complete_link(open(caminho_dados), KMin, KMax)
    print("Complete_link")
    for d in dados_complete_link:
        particao_complete_link = []
        for p in d:
            particao_complete_link.append(p[1])
        print(f'k = {max(particao_complete_link) + 1} {adjusted_rand_score(particao_real, particao_complete_link)}')

main()

