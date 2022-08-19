from tokenize import Number


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
    return label, data;