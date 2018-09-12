'''CARACTERÍSTICAS DO ESTADO'''


#10 - QUANTIDADE DE PROJETOS DIVISÍVEIS

def QprojDiv(self, p):                                      #Função recebe os projetos como parâmetro do Estado

    lpdiv = []                                              #Lista vazia que irá armazenar os projetos que são divisíveis
    contpdiv = 0                                            #Contador que irá armazenar a quantidade de projetos divisíveis
        for p in estado_x.P:                                #Para todos os projetos no conjunto de projetos 'P'
            if( p.vdiv == 1):                               #Se, vdiv for igual a 1, significa que o projeto é divisível
                lpdiv.append(p)                             #A lista recebe o projeto em questão
                contpdiv = contpdiv + 1                     #Acréscimo de 1 no contador
	
    print('Projetos Divisíveis: \n')                        #Impressão dos projetos divisíveis
        for p in self.lpdiv:
            print p.nome

    return contpdiv                                         #A função retorna o contador com a quantidade total de projetos em P capazes de serem divididos

''' AS FUNÇÕES 11 E 12 SEGUEM A MESMA LÓGICA DA 10, APENAS MUDANDO O NOME DE ALGUNS PARÂMETROS/VARIÁVEIS LOCAIS '''
	
#11 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ÁREA

def QprojDiva(self, p):

    lpdiva = []
    contpdiva = 0
        for p in estado_x.P_a[a]:
            if( p.vdiv == 1):
                lpdiva.append(p)
                contpdiva = contpdiva + 1
	
    print('Projetos Divisíveis: \n')
        for p in self.lpdiva:
            print p.nome

    return contpdiva
	
	
	
#12 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ETAPA DO FUNIL

def QprojDive(self, p):

    lpdive = []
    contpdive = 0
        for p in estado_x.P_e[e]:
            if( p.vdiv == 1):
                lpdive.append(p)
                contpdive = contpdive + 1
	
    print('Projetos Divisíveis: \n')
        for p in self.lpdive:
            print p.nome

    return contpdive
	
	
