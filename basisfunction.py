''' CARACTERISTICAS DO ESTADO '''


# QUANTIDADE DE PROJETOS DIVISIVEIS

def QprojDiv(estado_x):                                          #Funcao recebe os projetos como parametro do Estado

    lpdiv = []                                                   #Lista vazia que ira armazenar os projetos que sao divisiveis
    contpdiv = 0                                                 #Contador que ira armazenar a quantidade de projetos divisiveis
    for p in estado_x.P:                                         #Para todos os projetos no conjunto de projetos 'P'
        if( p.vdiv == 1):                                        #Se, vdiv for igual a 1, significa que o projeto e divisivel
            lpdiv.append(p)                                      #A lista recebe o projeto em questao
            contpdiv = contpdiv + 1                              #Acrescimo de 1 no contador
	
    print('Projetos Divisiveis: \n')                             #Impressao dos projetos divisiveis
    for p in self.lpdiv:
        print p.nome

    return contpdiv                                              #A funcao retorna o contador com a quantidade total de projetos em P capazes de serem divididos
	
#11 - QUANTIDADE DE PROJETOS DIVISIVEIS EM CADA AREA

def QprojDiva(estado_x):

    lpdiva = []
    contpdiva = 0
    for p in estado_x.P_a[a]:
        if( p.vdiv == 1):
            lpdiva.append(p)
            contpdiva = contpdiva + 1
	
    print('Projetos Divisiveis: \n')
    for p in self.lpdiva:
        print p.nome

    return contpdiva
	
	
	
#12 - QUANTIDADE DE PROJETOS DIVISIVEIS EM CADA ETAPA DO FUNIL

def QprojDive(estado_x):

    lpdive = []
    contpdive = 0
    for p in estado_x.P_e[e]:
        if( p.vdiv == 1):
            lpdive.append(p)
            contpdive = contpdive + 1
	
    print('Projetos Divisiveis: \n')
    for p in self.lpdive:
        print p.nome

    return contpdive
	
	
