# -*- coding: utf-8 -*-
from cStringIO import StringIO


''' CARACTERÍSTICAS DO ESTADO '''


#01 - QUANTIDADE TOTAL DE PROJETOS NO FUNIL

def QProj(estado_x):                                                                      #Função recebe o Estado como parâmetro

    contp = 0                                                                             #Contador que irá armazenar a quantidade de projetos total no funil
    for p in estado_x.P:                                                                  #Para todos os projetos no conjunto de projetos 'P'   
        contp = contp + 1                                                                 #Acréscimo de 1 no contador

    print ('Projetos no funil: \n')                                                       #Impressão dos projetos no funil
    for p in estado_x.P:
        print p.nome

    return contp                                                                          #A função retorna o contador com a quantidade total de projetos no funil



#02 - QUANTIDADE DE NOVOS PROJETOS ENTRANDO NO FUNIL

def QProjNovos(estado_x):                                                                 #Função recebe o Estado como parâmetro

    contpnovos = 0                                                                        #Contador que irá armazenar a quantidade de projetos novos
    contpestagio1 = 0                                                                     #Contador que irá armazenar a quantidade de projetos no estágio 1
    contpestagiox = 0                                                                     #Contador que irá armazenar a quantidade de projetos nos demais estágios
    contpcancelado = 0                                                                    #Contador que irá armazenar a quantidade de projetos cancelados
    contplancado = 0                                                                      #Contador que irá armazenar a quantidade de projetos lançados
    contaux = 0                                                                           #Contador auxiliar
    contpant = 0                                                                          #Contador do estágio anterior
    if(estado_x.estagio == 1):                                                            #Se está no primeiro estágio
        for p in estado_x.P:
            contpestagio1 = contpestagio1 + 1                                             #Contador do estágio 1 é acrescido de 1
        return contpnovos                                                                 #A função retorna zero, pois não há introdução de novos projetos no estágio 1
	
    else:                                                                                 #Se não
        for p in estado_x.P:
            contpestagiox = contpestagiox + 1                                             #É feita a contagem de projetos nesse estágio
            if(estado_x.y[p] > 0):
                contpcancelado = contpcancelado + 1                                       #Dos projetos que foram cancelados
            
        for p in estado_x.Pl:
            contplancado = contplancado + 1                                               #Dos projetos que foram lançados

    if(estado_x.estagio == 2):                                                            #Se está no segundo estágio
        contpant = contpestagio1                                                          #Contador do estágio anterior recebe o valor do estágio 1
    
    else:                                                                                 #Se não
        contpant = contpestagiox                                                          #Contador do estágio anterior recebe o valor do estágio (atual - 1)

    contaux = contpant - contpcancelado - contplancado                                    #Contador auxiliar armazena a diferença entre a quantidade no estágio anterior e dos cancelados/lançados
    contpnovos = contpestagiox - contaux                                                  #Por fim, o contador de novos projetos recebe a diferença entre total do estágio e do auxiliar, que é quantidade de novos projetos
    return contpnovos                                                                     #A função retorna o contador com a quantidade total de novos projetos no funil



#03 - QUANTIDADE DE PROJETOS POR ETAPA DO FUNIL

def QProje(estado_x):                                                                     #Função recebe o Estado como parâmetro

    contpe = 0                                                                            #Contador que irá armazenar a quantidade de projetos por etapa do funil
    lpe = []                                                                              #Lista que irá armazenar as quantidades de projetos por etapa do funil
    lpenome = []                                                                          #Lista que irá armazenar o nome dos projetos por etapa do funil

    for e in estado_x.E:                                                                  #Para todo estado no conjunto de Estados
        for p in estado_x.P_e[e]:                                                         #Para todo projeto em cada estado 'e'
            contpe = contpe + 1                                                           #Contador recebe o acréscimo de 1
            lpenome.append(p)                                                             #O projeto é adicionado na lista
        lpe.append(contpe)                                                                #A quantidade de projetos no estado 'e' é adicionada a lista de quantidades
        contpe = 0
        print('Projetos na etapa' + str(p.etapa) + '\n')                                  #Impressão dos projetos na etapa 'e'
        for p in self.lpenome:
            print p.nome

    return lpe                                                                            #A função retorna a lista de quantidades de projetos por etapa 'e'



#04 - QUANTIDADE DE RECURSOS ALOCADOS NO FUNIL

def QRecAloc(estado_x):                                                                   #Função recebe o Estado como parâmetro

    qtotal = 0
    for e in estado_x.E:                                                                  #Para todo etapa no conjunto de Etapas do funil
        qtotal = qtotal + estado_x.tn[e]                                                  #qtotal recebe os valores alocados por etapa

    return qtotal                                                                         #A função retorna qtotal com a quantidade total de recursos alocados em todas as etapas do funil



#05 - QUANTIDADE DE RECURSOS ALOCADOS EM CADA ETAPA DO FUNIL

def QRecAloce(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lqtotale = []                                                                         #Lista que irá armazenar as quantidades alocadas em cada etapa do funil
    for e in estado_x.E:                                                                  #Para cada etapa no conjunto de Etapas do funil
        lqtotale.append(estado_x.tn[e])                                                   #Lista recebendo os valores

    return lqtotale                                                                       #A função retorna lqtotal que é a lista com todos os valores alocados por etapa no funil



#06 - QUANTIDADE DE PROJETOS POR ÁREA DO FUNIL

def QProja(estado_x):                                                                     #Função recebe o Estado como parâmetro

    contpa = 0                                                                            #Contador que irá armazenar a quantidade de projetos por área do funil
    lpa = []                                                                              #Lista que irá armazenar as quantidades de projetos por área do funil
    lpanome = []                                                                          #Lista que irá armazenar o nome dos projetos por área do funil
    for a in estado_x.A:                                                                  #Para toda área no conjunto de Áreas
        for p in estado_x.P_a[a]:                                                         #Para todo projeto em cada área 'a'
            contpe = contpe + 1                                                           #Contador recebe o acréscimo de 1
            lpanome.append(p)                                                             #O projeto é adicionado na lista
        lpa.append(contpa)                                                                #A quantidade de projetos na área 'a' é adicionada a lista de quantidades
        contpa = 0
        print('Projetos na área' + str(p.area) + '\n')                                    #Impressão dos projetos na área 'a'
        for p in self.lpanome:
            print p.nome

    return lpa                                                                            #A função retorna a lista de quantidades de projetos por área 'a'



#07 - QUANTIDADE DE RECURSOS ALOCADOS EM CADA ÁREA 

def QReca(estado_x):                                                                      #Função recebe o Estado como parâmetro

    somap = 0                                                                             #Irá somar o valor gasto por etapa do projeto
    lsomap = []                                                                           #Lista que irá armazenar o valor dos projetos de uma área 'a'
    lsomafinal = []                                                                       #Lista que irá armazenar os valores de cada área 'a'
    for a in estado_x.A:                                                                  #Para toda área
        for p in estado_x.P_a[a]:                                                         #Para todo projeto na área 'a'
            for e in estado_x.E:                                                          #Para toda etapa do projeto P[a]
                somap = somap + p.modos[p.etapa -1][mod].nrn                              #Soma o custo do modo que ele foi executado

            lsomap.append(somap)                                                          #A soma dos custos é adicionada em uma lista de projetos da área 'a'

        lsomafinal.append(sum(lsomap))                                                    #A soma de cada área é adicionada em uma lista de todas as áreas 'a'

    return lsomafinal                                                                     #A função retorna a lista de recursos alocados em cada área 'a'



#08 - QUANTIDADE DE PROJETOS DE CADA ÁREA POR ETAPA DO FUNIL

def QProjae(estado_x):                                                                    #Função recebe o Estado como parâmetro

    contpae = 0                                                                           #Contador que irá armazenar a quantidade de projetos em cada área por etapa do funil
    lpaenome = []                                                                         #Lista que irá armazenar os projetos de uma área por etapa do funil
    lpae = []                                                                             #Lista que irá armazenar as quantidades de proejtos das áreas por etapa do funil
    for e in estado_x.E:                                                                  #Para todo estado no conjunto de Estados                                                             
        for a in estado_x.A:                                                              #Para toda área no conjunto de Áreas
            for p in estado_x.P_a[a]:                                                     #Para todo projeto no conjunto de Projetos por Área
                contpae = contpae + 1                                                     #Contador recebe o acréscimo de mais 1
                lpaenome.append(p)                                                        #Lista de nome recebe o projeto
            lpae.append(contpae)                                                          #Lista de quantidades recebe o contador
            contpae = 0
        print('Projetos na área' + str(p.area) + 'da etapa'+ str(p.etapa) + '\n')         #Impressão dos projetos por área em cada etapa do funil
        for p in self.lpaenome:
            print p.nome

    return lpae                                                                           #A função retorna a lista com as quantidades



#09 - QUANTIDADE DE RECURSOS ALOCADOS POR ÁREA EM CADA ETAPA DO FUNIL

def QRecae(estado_x):                                                                      #Função recebe o Estado como parâmetro

    lvalorp = []                                                                           #Lista que irá receber os valores de cada projeto por área e etapa do funil
    lvalora = []                                                                           #Lista que irá receber os valores por área
    lvalore = []                                                                           #Lista que irá receber os valores por etapa de cada área
    for e in estado_x.E:                                                                   #Para todo etapa 'e'
        for a in estado_x.A:                                                               #Para toda área 'a'
            for p in estado_x.P_a[a]:                                                      #Para todo projeto na área 'a'
                lvalorp.append(p.modos[p.etapa -1][mod].nrn)                               #Lista recebe cada recurso alocado na área 'a' e etapa 'e' do projeto 'p'

            lvalora.append(sum(lvalorp))                                                   #Lista recebe o somatório dos recursos alocados para a área 'a'

        lvalore.append(lvalora)                                                            #Lista recebe o valor alocado em cada área por etapa 'e'

    return lvalore                                                                         #A função retorna a lista de recursos alocados



#10 - QUANTIDADE DE PROJETOS DIVISÍVEIS

def QProjDiv(estado_x):                                                                   #Função recebe o Estado como parâmetro

    lpdiv = []                                                                            #Lista vazia que irá armazenar os projetos que são divisíveis
    contpdiv = 0                                                                          #Contador que irá armazenar a quantidade de projetos divisíveis
    for p in estado_x.P:                                                                  #Para todos os projetos no conjunto de projetos 'P'
        if( p.vdiv == 1):                                                                 #Se, vdiv for igual a 1, significa que o projeto é divisível
            lpdiv.append(p)                                                               #A lista recebe o projeto em questão
            contpdiv = contpdiv + 1                                                       #Acréscimo de 1 no contador
	
    print('Projetos Divisíveis: \n')                                                      #Impressão dos projetos divisíveis
    for p in self.lpdiv:
        print p.nome

    return contpdiv                                                                       #A função retorna o contador com a quantidade total de projetos em P capazes de serem divididos



#11 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ÁREA

def QProjDiva(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lpdiva = []                                                                           #Lista para armazenar as quantidades de projetos divisíveis por área      
    lpdivanome = []                                                                       #Lista para armazenar os projetos divisíveis por área
    contpdiva = 0                                                                         #Contador dos projetos divisíveis por área
    for a in estado_x.A:                                                                  #Para toda área do conjunto de Áreas
        for p in estado_x.P_a[a]:                                                         #Para todo projeto na área 'a'
            if( p.vdiv == 1):                                                             #Se ele for divisível
                lpdivanome.append(p)                                                      #Entra na lista 
                contpdiva = contpdiva + 1                                                 #Acréscimo de 1 no contador
        lpdiva.append(contpdiva)                                                          #A lista de quantidades recebe contpdiva
        contpdiva = 0

        print('Projetos Divisíveis na área'+ str(p.area) +'\n')                           #Impressão dos projetos divisíveis por área
        for p in self.lpdivanome:
            print p.nome

    return lpdiva                                                                         #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



#12 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ETAPA DO FUNIL

def QProjDive(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lpdive = []                                                                           #Lista para armazenar as quantidades de projetos divisíveis por etapa
    lpdivenome = []                                                                       #Lista para armazenar os projetos divisíveis por etapa
    contpdive = 0                                                                         #Contador dos projetos divisíveis por etapa
    for e in estado_x.E:                                                                  #Para toda etapa do conjunto de Etapas
        for p in estado_x.P_e[e]:                                                         #Para todo projeto na etapa 'e'
            if( p.vdiv == 1):                                                             #Se ele for divisível
                lpdivenome.append(p)                                                      #Entra na lista
                contpdive = contpdive + 1                                                 #Acréscimo de 1 no contador

        lpdive.append(contpdive)                                                          #A lista de quantidades recebe contpdive
        contpdive = 0
	
        print('Projetos Divisíveis na etapa'+ str(p.etapa)+'\n')                          #Impressão dos projetos divisíveis por etapa 
        for p in self.lpdivenome:
            print p.nome

    return lpdive                                                                         #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



#13 - QUANTIDADE DE PROJETOS NÃO-DIVISÍVEIS

def QProjnDiv(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lpndiv = []                                                                           #Lista vazia que irá armazenar os projetos que não são divisíveis
    contpndiv = 0                                                                         #Contador que irá armazenar a quantidade de projetos não divisíveis
    for p in estado_x.P:                                                                  #Para todos os projetos no conjunto de projetos 'P'
        if( p.vdiv != 1):                                                                 #Se, vdiv for diferente de 1, significa que o projeto não é divisível
            lpdiv.append(p)                                                               #A lista recebe o projeto em questão
            contpdiv = contpdiv + 1                                                       #Acréscimo de 1 no contador
	
    print('Projetos não Divisíveis: \n')                                                  #Impressão dos projetos não divisíveis
    for p in self.lpndiv:
        print p.nome

    return contpndiv                                                                      #A função retorna o contador com a quantidade total de projetos em P não divisíveis



#14 - TEMPO DE CONGELAMENTO TOTAL DE CADA PROJETO

def TCongP(estado_x):                                                                     #Função recebe o Estado como parâmetro

    lpdivl = []                                                                           #Lista vazia que irá armazenar os projetos divisíveis
    ltempo = []                                                                           #Lista vazia que irá armazenar os tempos congelados de cada projeto
    for p in estado_x.Pl:                                                                 #Para todo projeto lançado
        if(p.vdiv == 1):                                                                  #Se for divisível
            lpdivl.append(p)                                                              #Lista recebe os projetos 

    for p in self.lpdivl:                                                                 #Para todo projeto divisível
        print('Tempo de congelamento total de' + str(p.nome) + ': \n')                    #Imprime o nome e seu tempo congelado
        print p.congatual
        ltempo.append(p.congatual)                                                        #A lista recebe os tempos de congelamento de cada projeto lançado

    return ltempo                                                                         #A função retorna os tempos congelados de cada projeto



#15 - TEMPO DE CONGELAMENTO RESIDUAL DE CADA PROJETO

def TCongReP(estado_x):                                                                   #Função recebe o Estado como parâmetro

    laux = []                                                                             #Lista que irá armazenar os projetos divisíveis
    residual = 0                                                                          #Variável que irá armazenar os tempos residuais
    lresidual = []                                                                        #Lista que irá armazenar os tempos residuais de cada projeto
    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos
        if(p.vdiv == 1):                                                                  #Se o projeto for divisível
            laux.append(p)                                                                #Lista armazena o projeto
            residual = p.cmax - p.congatual                                               #Residual recebe a diferença do tempo máximo e o congelamento atual
            lresidual.append(residual)                                                    #Lista armazena os tempos residuais de cada projeto

    return lresidual                                                                      #A função retorna os tempos residuais de congelamento de cada projeto






















