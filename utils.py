def readTableTxt(arq):
    data = []
    linhas = arq.readlines()

    primeira_linha_string = True
    for i in linhas[0].split():
        if(i.isdigit()):
            primeira_linha_string = False
            break
    if(primeira_linha_string):
        linhas.pop(0)
    for linha in linhas:
        l = linha.split()
        for i in range(0, len(l)):
            if(l[i].replace('.','',1).replace('-','',1).isnumeric()):
                l[i] = float(l[i])
        data.append(l)
    return data

def flat(l):
    return [item for sublist in l for item in sublist]

def escrever_particao_no_arquivo(caminho, particao):
    p = []
    with open(caminho, "w") as arq:
        for cluster in particao:
            cluster.sort(key=__compar)
            for obj in cluster:
                arq.write("{:<10} {:<1}\n".format(obj, particao.index(cluster)))
                p.append([obj, particao.index(cluster)])
    return p

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
