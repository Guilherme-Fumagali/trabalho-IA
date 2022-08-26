import k_means
import single_complete_link

def main():
    arq = open("/home/gfumagali/Documents/Trabalho IA/trabalho-IA/datasets/simpsons.txt");
    k_means.k_means(arq, 2, 10)
    arq = open("/home/gfumagali/Documents/Trabalho IA/trabalho-IA/datasets/simpsons.txt");
    single_complete_link.single_link(arq, 2, 5)
    arq = open("/home/gfumagali/Documents/Trabalho IA/trabalho-IA/datasets/simpsons.txt");
    single_complete_link.complete_link(arq, 2, 5)

main()