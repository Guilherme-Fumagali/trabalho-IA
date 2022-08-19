def readTables(caminho_arquivo):
    data = []
    arq = open(caminho_arquivo)
    linhas = arq.readlines()
    label = linhas[0].split()
    for linha in linhas:
        data.append(linha.split())
    data.remove(label)
    return label, data;