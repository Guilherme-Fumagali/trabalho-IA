""" 
Grupo 01

Guilherme Fumagali Marques       - 792182 
Guilherme Silva de Camargo       - 792183
Rodrigo Henrique Amaral Araújo   - 792241 
Vinicius Gabriel Nanini da Silva - 795181

Arquivo com as funções auxiliares para manipulação dos dados
"""

""" Recebe um arquivo e o armazena em memória """
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

""" Recebe um vetor em mais de uma dimensão e o retorna em uma dimensão """
def flat(l):
    return [item for sublist in l for item in sublist]

""" Recebe uma partição e o escreve no arquivo segundo o caminho """
def escrever_particao_no_arquivo(caminho, particao):
    objetos = []
    for cluster in particao:
        for obj in cluster:
            objetos.append([obj, particao.index(cluster)])
    objetos.sort(key=__compar)
    with open(caminho, "w") as arq:
        for obj in objetos:
            arq.write("{:<10} {:<1}\n".format(obj[0], obj[1]))
    return objetos

""" Função de comparação auxiliar ao sort() """
def __compar(x):
    x = flat(x[0])
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
