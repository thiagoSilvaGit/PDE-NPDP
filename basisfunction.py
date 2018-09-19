# -*- coding: utf-8 -*-
from cStringIO import StringIO


''' CARACTERÍSTICAS DO ESTADO '''


#01 - QUANTIDADE TOTAL DE PROJETOS NO FUNIL

def Qproj(estado_x):                                                 #Função recebe o Estado como parâmetro

    contp = 0                                                        #Contador que irá armazenar a quantidade de projetos total no funil
    for p in estado_x.P:                                             #Para todos os projetos no conjunto de projetos 'P'   
        contp = contp + 1                                            #Acréscimo de 1 no contador

    print ('Projetos no funil: \n')                                  #Impressão dos projetos no funil
    for p in estado_x.P:
        print p.nome

    return contp                                                     #A função retorna o contador com a quantidade total de projetos no funil



#02 - QUANTIDADE DE NOVOS PROJETOS ENTRANDO NO FUNIL

def QprojNovos(estado_x):                                            #Função recebe o Estado como parâmetro

    contpnovos = 0                                                   #Contador que irá armazenar a quantidade de projetos novos
    contpestagio1 = 0                                                #Contador que irá armazenar a quantidade de projetos no estágio 1
    contpestagiox = 0                                                #Contador que irá armazenar a quantidade de projetos nos demais estágios
    contpcancelado = 0                                               #Contador que irá armazenar a quantidade de projetos cancelados
    contplancado = 0                                                 #Contador que irá armazenar a quantidade de projetos lançados
    contaux = 0                                                      #Contador auxiliar
    contpant = 0                                                     #Contador do estágio anterior
    if(estado_x.estagio == 1):                                       #Se está no primeiro estágio
        for p in estado_x.P:
            contpestagio1 = contpestagio1 + 1                        #Contador do estágio 1 é acrescido de 1
        return contpnovos                                            #A função retorna zero, pois não há introdução de novos projetos no estágio 1
	
    else:                                                            #Se não
        for p in estado_x.P:
            contpestagiox = contpestagiox + 1                        #É feita a contagem de projetos nesse estágio
            if(estado_x.y[p] > 0):
                contpcancelado = contpcancelado + 1                  #Dos projetos que foram cancelados
            
        for p in estado_x.Pl:
            contplancado = contplancado + 1                          #Dos projetos que foram lançados

    if(estado_x.estagio == 2):                                       #Se está no segundo estágio
        contpant = contpestagio1                                     #Contador do estágio anterior recebe o valor do estágio 1
    
    else:                                                            #Se não
        contpant = contpestagiox                                     #Contador do estágio anterior recebe o valor do estágio (atual - 1)

    contaux = contpant - contpcancelado - contplancado               #Contador auxiliar armazena a diferença entre a quantidade no estágio anterior e dos cancelados/lançados
    contpnovos = contpestagiox - contaux                             #Por fim, o contador de novos projetos recebe a diferença entre total do estágio e do auxiliar, que é quantidade de novos projetos
    return contpnovos                                                #A função retorna o contador com a quantidade total de novos projetos no funil



#03 - QUANTIDADE DE PROJETOS POR ETAPA DO FUNIL

def Qproje(estado_x):                                                #Função recebe o Estado como parâmetro

    contpe = 0                                                       #Contador que irá armazenar a quantidade de projetos por etapa do funil
    lpe = []                                                         #Lista que irá armazenar as quantidades de projetos por etapa do funil
    lpenome = []                                                     #Lista que irá armazenar o nome dos projetos por etapa do funil

    for e in estado_x.E:                                             #Para todo estado no conjunto de Estados
        for p in estado_x.P_e[e]:                                    #Para todo projeto em cada estado 'e'
            contpe = contpe + 1                                      #Contador recebe o acréscimo de 1
            lpenome.append(p)                                        #O projeto é adicionado na lista
        lpe.append(contpe)                                           #A quantidade de projetos no estado 'e' é adicionada a lista de quantidades
        contpe = 0
        print('Projetos na etapa' + str(p.etapa) + '\n')             #Impressão dos projetos na etapa 'e'
        for p in self.lpenome:
            print p.nome

    return lpe                                                       #A função retorna a lista de quantidades de projetos por etapa 'e'



#04 - QUANTIDADE DE RECURSOS ALOCADOS NO FUNIL

def Qrecaloc(estado_x):                                              #Função recebe o Estado como parâmetro

    qtotal = 0
    for e in estado_x.E:                                             #Para todo etapa no conjunto de Etapas do funil
        qtotal = qtotal + estado_x.tn[e]                             #qtotal recebe os valores alocados por etapa

    return qtotal                                                    #A função retorna qtotal com a quantidade total de recursos alocados em todas as etapas do funil



#05 - QUANTIDADE DE RECURSOS ALOCADOS EM CADA ETAPA DO FUNIL

def Qrecaloce(estado_x):                                             #Função recebe o Estado como parâmetro

    lqtotal = []                                                     #Lista que irá armazenar as quantidades alocadas em cada etapa do funil
    for e in estado_x.E:                                             #Para cada etapa no conjunto de Etapas do funil
        lqtotal.append(estado_x.tn[e])                               #Lista recebendo os valores

    return lqtotal                                                   #A função retorna lqtotal que é a lista com todos os valores alocados por etapa no funil



#10 - QUANTIDADE DE PROJETOS DIVISÍVEIS

def QprojDiv(estado_x):                                              #Função recebe o Estado como parâmetro

    lpdiv = []                                                       #Lista vazia que irá armazenar os projetos que são divisíveis
    contpdiv = 0                                                     #Contador que irá armazenar a quantidade de projetos divisíveis
    for p in estado_x.P:                                             #Para todos os projetos no conjunto de projetos 'P'
        if( p.vdiv == 1):                                            #Se, vdiv for igual a 1, significa que o projeto e divisível
            lpdiv.append(p)                                          #A lista recebe o projeto em questão
            contpdiv = contpdiv + 1                                  #Acréscimo de 1 no contador
	
    print('Projetos Divisíveis: \n')                                 #Impressão dos projetos divisíveis
    for p in self.lpdiv:
        print p.nome

    return contpdiv                                                  #A função retorna o contador com a quantidade total de projetos em P capazes de serem divididos



#11 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ÁREA

def QprojDiva(estado_x):                                             #Função recebe o Estado como parâmetro

    lpdiva = []                                                      #Lista para armazenar as quantidades de projetos divisíveis por área      
    lpdivanome = []                                                  #Lista para armazenar os projetos divisíveis por área
    contpdiva = 0                                                    #Contador dos projetos divisíveis por área
    for a in estado_x.A:                                             #Para toda área do conjunto de Áreas
        for p in estado_x.P_a[a]:                                    #Para todo projeto na área 'a'
            if( p.vdiv == 1):                                        #Se ele for divisível
                lpdivanome.append(p)                                 #Entra na lista 
                contpdiva = contpdiva + 1                            #Acréscimo de 1 no contador
        lpdiva.append(contpdiva)                                     #A lista de quantidades recebe contpdiva
        contpdiva = 0

        print('Projetos Divisíveis na área'+ str(p.area) +'\n')     #Impressão dos projetos divisíveis por área
        for p in self.lpdivanome:
            print p.nome

    return lpdiva                                                    #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



#12 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ETAPA DO FUNIL

def QprojDive(estado_x):                                             #Função recebe o Estado como parâmetro

    lpdive = []                                                      #Lista para armazenar as quantidades de projetos divisíveis por etapa
    lpdivenome = []                                                  #Lista para armazenar os projetos divisíveis por etapa
    contpdive = 0                                                    #Contador dos projetos divisíveis por etapa
    for e in estado_x.E:                                             #Para toda etapa do conjunto de Etapas
        for p in estado_x.P_e[e]:                                    #Para todo projeto na etapa 'e'
            if( p.vdiv == 1):                                        #Se ele for divisível
                lpdivenome.append(p)                                 #Entra na lista
                contpdive = contpdive + 1                            #Acréscimo de 1 no contador

        lpdive.append(contpdive)                                     #A lista de quantidades recebe contpdive
        contpdive = 0
	
        print('Projetos Divisíveis na etapa'+ str(p.etapa)+'\n')     #Impressão dos projetos divisíveis por etapa 
        for p in self.lpdivenome:
            print p.nome

    return lpdive                                                    #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil


