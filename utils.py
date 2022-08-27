def readTableTxt(arq):
    data = []
    linhas = arq.readlines()
    label = linhas[0].split()
    for linha in linhas:
        l = linha.split()
        for i in range(0, len(l)):
            if(l[i].replace('.','',1).isdigit()):
                l[i] = float(l[i])
        data.append(l)
    data.remove(label)
    return label, data

def flat(l):
    return [item for sublist in l for item in sublist]

def escrever_particao_no_arquivo(caminho, particao):
    with open(caminho, "w") as arq:
        for cluster in particao:
            cluster.sort(key=__compar)
            for obj in cluster:
                arq.write("{:<10} {:<1}\n".format(obj, particao.index(cluster)))

def __compar(x):
    x = flat(x)
    letras = ""
    numeros = ""
    for i in x:
        if(i.isdigit()):
            numeros += i
        else:
            letras += i
    if len(numeros) > 0:
        return int(numeros)
    else:
        return letras
