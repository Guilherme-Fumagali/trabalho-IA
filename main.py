from operator import truediv
from random import random
import utils 

def k_means(arq, k, iteracoes):
    label, datas = utils.readTableTxt(arq);
    
    clusters = []
    for i in range(0, k):
        while(True):
            obj = datas[int((len(datas) - 1) * random())];
            if obj not in clusters:
                clusters.append(obj)
                break
    print(clusters)
   

arq = open("/home/gfumagali/Documents/Trabalho IA/trabalho-IA/datasets/simpsons.txt");
k_means(arq, 3, 10);