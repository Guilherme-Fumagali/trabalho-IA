import k_means
import single_complete_link

def main():
    caminho = "datasets\c2ds1-2sp.txt"
    arq = open(caminho);
    k_means.k_means(arq, 2, 10)
    arq = open(caminho);
    single_complete_link.single_link(arq, 2, 5)
    arq = open(caminho);
    single_complete_link.complete_link(arq, 2, 5)

main()