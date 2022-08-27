import k_means
import utils
import single_complete_link
from sklearn.metrics.cluster import adjusted_rand_score

def main():
    caminho_dados = "datasets\c2ds1-2sp.txt"
    caminho_clusters_real = "datasets\c2ds1-2spReal.clu"

    #Obtendo partição real
    dados_reais = utils.readTableTxt(open(caminho_clusters_real))
    particao_real = []
    for d in dados_reais:
        particao_real.append(d[0])

    #k-medias
    particao_k_medias = k_means.k_means(open(caminho_dados), 2, 1)
    print()
    print(f"K-medias: {adjusted_rand_score(particao_real, utils.flat(particao_k_medias))}")

    #Single-link
    particoes_single_link = single_complete_link.single_link(open(caminho_dados), 2, 5)
    print("Single-link")
    for p in particoes_single_link:
        print(f'k = {len(p)} {adjusted_rand_score(particao_real, utils.flat(p))}')

    return
    arq = open(caminho);
    single_complete_link.complete_link(arq, 2, 5)

main()

