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
    mediaqp = 0                                                                           #Recebe a média das listas

    for e in estado_x.E:                                                                  #Para todo estado no conjunto de Estados
        for p in estado_x.P_e[e]:                                                         #Para todo projeto em cada estado 'e'
            contpe = contpe + 1                                                           #Contador recebe o acréscimo de 1
            lpenome.append(p)                                                             #O projeto é adicionado na lista
        lpe.append(contpe)                                                                #A quantidade de projetos no estado 'e' é adicionada a lista de quantidades
        contpe = 0
        print('Projetos na etapa' + str(p.etapa) + '\n')                                  #Impressão dos projetos na etapa 'e'
        for p in self.lpenome:
            print p.nome

    mediaqp = (sum(lpe)/len(lpe))

    return mediaqp                                                                        #A função retorna a lista de quantidades de projetos por etapa 'e'



#04 - QUANTIDADE DE RECURSOS ALOCADOS NO FUNIL

def QRecAloc(estado_x):                                                                   #Função recebe o Estado como parâmetro

    qtotal = 0
    for e in estado_x.E:                                                                  #Para todo etapa no conjunto de Etapas do funil
        qtotal = qtotal + estado_x.tn[e]                                                  #qtotal recebe os valores alocados por etapa

    return qtotal                                                                         #A função retorna qtotal com a quantidade total de recursos alocados em todas as etapas do funil



#05 - QUANTIDADE DE RECURSOS ALOCADOS EM CADA ETAPA DO FUNIL

def QRecAloce(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lqtotale = []                                                                         #Lista que irá armazenar as quantidades alocadas em cada etapa do funil
    mediaqr = 0                                                                           #Recebe a média das listas
    for e in estado_x.E:                                                                  #Para cada etapa no conjunto de Etapas do funil
        lqtotale.append(estado_x.tn[e])                                                   #Lista recebendo os valores

    mediaqr = (sum(lqtotale)/len(lqtotale))

    return mediaqr                                                                        #A função retorna lqtotal que é a lista com todos os valores alocados por etapa no funil



#06 - QUANTIDADE DE PROJETOS POR ÁREA DO FUNIL

def QProja(estado_x):                                                                     #Função recebe o Estado como parâmetro

    contpa = 0                                                                            #Contador que irá armazenar a quantidade de projetos por área do funil
    lpa = []                                                                              #Lista que irá armazenar as quantidades de projetos por área do funil
    mediaqa = 0                                                                           #Recebe a média das listas
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

    mediaqa = (sum(lpa)/len(lpa))

    return mediaqa                                                                        #A função retorna a lista de quantidades de projetos por área 'a'



#07 - QUANTIDADE DE RECURSOS ALOCADOS EM CADA ÁREA 

def QReca(estado_x):                                                                      #Função recebe o Estado como parâmetro

    somap = 0                                                                             #Irá somar o valor gasto por etapa do projeto
    lsomap = []                                                                           #Lista que irá armazenar o valor dos projetos de uma área 'a'
    lsomafinal = []                                                                       #Lista que irá armazenar os valores de cada área 'a'
    mediasf = 0                                                                           #Recebe a média das listas
    for a in estado_x.A:                                                                  #Para toda área
        for p in estado_x.P_a[a]:                                                         #Para todo projeto na área 'a'
            for e in estado_x.E:                                                          #Para toda etapa do projeto P[a]
                somap = somap + p.modos[p.etapa -1][mod].nrn                              #Soma o custo do modo que ele foi executado

            lsomap.append(somap)                                                          #A soma dos custos é adicionada em uma lista de projetos da área 'a'

        lsomafinal.append(sum(lsomap))                                                    #A soma de cada área é adicionada em uma lista de todas as áreas 'a'

    mediasf = (sum(lsomafinal)/len(lsomafinal))

    return mediasf                                                                        #A função retorna a lista de recursos alocados em cada área 'a'



#08 - QUANTIDADE DE PROJETOS DE CADA ÁREA POR ETAPA DO FUNIL

def QProjae(estado_x):                                                                    #Função recebe o Estado como parâmetro

    contpae = 0                                                                           #Contador que irá armazenar a quantidade de projetos em cada área por etapa do funil
    lpaenome = []                                                                         #Lista que irá armazenar os projetos de uma área por etapa do funil
    lpae = []                                                                             #Lista que irá armazenar as quantidades de proejtos das áreas por etapa do funil
    mediaae = 0                                                                           #Recebe a média das listas
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

    mediaae = (sum(lpae)/len(lpae))

    return mediaae                                                                        #A função retorna a lista com as quantidades



#09 - QUANTIDADE DE RECURSOS ALOCADOS POR ÁREA EM CADA ETAPA DO FUNIL

def QRecae(estado_x):                                                                      #Função recebe o Estado como parâmetro

    lvalorp = []                                                                           #Lista que irá receber os valores de cada projeto por área e etapa do funil
    lvalora = []                                                                           #Lista que irá receber os valores por área
    lvalore = []                                                                           #Lista que irá receber os valores por etapa de cada área
    mediave = 0                                                                            #Recebe a média das listas
    for e in estado_x.E:                                                                   #Para todo etapa 'e'
        for a in estado_x.A:                                                               #Para toda área 'a'
            for p in estado_x.P_a[a]:                                                      #Para todo projeto na área 'a'
                lvalorp.append(p.modos[p.etapa -1][mod].nrn)                               #Lista recebe cada recurso alocado na área 'a' e etapa 'e' do projeto 'p'

            lvalora.append(sum(lvalorp))                                                   #Lista recebe o somatório dos recursos alocados para a área 'a'

        lvalore.append(lvalora)                                                            #Lista recebe o valor alocado em cada área por etapa 'e'

    mediave = (sum(lvalore)/len(lvalore))

    return mediave                                                                         #A função retorna a lista de recursos alocados



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
    mediada = 0                                                                           #Recebe a média das listas
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

    mediada = (sum(lpdiva)/len(lpdiva))

    return mediada                                                                        #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



#12 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ETAPA DO FUNIL

def QProjDive(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lpdive = []                                                                           #Lista para armazenar as quantidades de projetos divisíveis por etapa
    lpdivenome = []                                                                       #Lista para armazenar os projetos divisíveis por etapa
    contpdive = 0                                                                         #Contador dos projetos divisíveis por etapa
    mediade = 0                                                                           #Recebe a média das listas
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

    mediade = (sum(lpdive)/len(lpdive))

    return mediade                                                                        #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



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
    mediat = 0                                                                            #Recebe a média das listas
    for p in estado_x.Pl:                                                                 #Para todo projeto lançado
        if(p.vdiv == 1):                                                                  #Se for divisível
            lpdivl.append(p)                                                              #Lista recebe os projetos 

    for p in self.lpdivl:                                                                 #Para todo projeto divisível
        print('Tempo de congelamento total de' + str(p.nome) + ': \n')                    #Imprime o nome e seu tempo congelado
        print p.congatual
        ltempo.append(p.congatual)                                                        #A lista recebe os tempos de congelamento de cada projeto lançado

    mediat = (sum(ltempo)/len(ltempo))

    return mediat                                                                         #A função retorna os tempos congelados de cada projeto



#15 - TEMPO DE CONGELAMENTO RESIDUAL DE CADA PROJETO

def TCongReP(estado_x):                                                                   #Função recebe o Estado como parâmetro

    laux = []                                                                             #Lista que irá armazenar os projetos divisíveis
    residual = 0                                                                          #Variável que irá armazenar os tempos residuais
    mediare = 0                                                                           #Recebe a média das listas
    lresidual = []                                                                        #Lista que irá armazenar os tempos residuais de cada projeto
    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos
        if(p.vdiv == 1):                                                                  #Se o projeto for divisível
            laux.append(p)                                                                #Lista armazena o projeto
            residual = p.cmax - p.congatual                                               #Residual recebe a diferença do tempo máximo e o congelamento atual
            lresidual.append(residual)                                                    #Lista armazena os tempos residuais de cada projeto

    mediare = (sum(lresidual)/len(lresidual))

    return mediare                                                                        #A função retorna os tempos residuais de congelamento de cada projeto



#16 - TEMPO RESIDUAL DE CADA PROJETO NO FUNIL

def TReP(estado_x):                                                                       #Função recebe o Estado como parâmetro

    ltr = []                                                                              #Lista que irá armazenar os tempos residuais
    mediatr = 0                                                                           #Recebe a média das listas
    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos 
        ltr.append(sum(ltempo) - p.Qexec)                                                 #A lista recebe a diferença entre o somatório total de tempos e o a quantidade executada: CRIAR ESSE PARÂMENTRO NO CÓDIGO

    mediatr = (sum(ltr)/len(ltr))

    return mediatr                                                                        #A função retorna os tempos residuais de cada projeto



#17 - TEMPO RESIDUAL DE CADA PROJETO POR ETAPA DO FUNIL

def TRePe(estado_x):                                                                      #Função recebe o Estado como parâmetro

    ltr = []                                                                              #Lista que irá armazenar os tempos residuais
    mediatr2 = 0                                                                          #Recebe a média das listas
    for e in estado_x.E:                                                                  #Para toda etapa no conjunto de Etapas 
        for p in estado_x.P[e]:                                                           #Para todo projeto no conjunto de projetos                                                                
            ltr.append(sum(ltempo) - p.Qexec)                                             #A lista recebe a diferença entre o somatório total de tempos e o a quantidade executada: CRIAR ESSE PARÂMENTRO NO CÓDIGO                                                

    mediatr2 = (sum(ltr)/len(ltr))

    return mediatr2                                                                       #A função retorna os tempos residuais de cada projeto                                                                           



#18 - TEMPO RESIDUAL DE CADA PROJETO POR ÁREA

def TRePa(estado_x):                                                                      #Função recebe o Estado como parâmetro

    ltr = []                                                                              #Lista que irá armazenar os tempos residuais
    mediatr3 = 0                                                                          #Recebe a média das listas
    for a in estado_x.A:                                                                  #Para toda área no conjunto de Áreas 
        for p in estado_x.P[a]:                                                           #Para todo projeto no conjunto de projetos                                                                
            ltr.append(sum(ltempo) - p.Qexec)                                             #A lista recebe a diferença entre o somatório total de tempos e o a quantidade executada: CRIAR ESSE PARÂMENTRO NO CÓDIGO                                                

    mediatr3 = (sum(ltr)/len(ltr))

    return mediatr3                                                                       #A função retorna os tempos residuais de cada projeto


#19 - NECESSIDADE DE RECURSOS DE CADA PROJETO

def NecRecP(estado_x):                                                                    #Função recebe o Estado como parâmetro

    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos 
        if (estado_x.M.quant > 2):                                                        #Se houver o modo Acelerar, imprime os três modos
            print('Necessidade de recursos do projeto' + str(p.nome) + 'é de:'+ 
            p.lnrn[0] +'para Continuar, '+ p.lnrn[1] +'para Melhorar e' + p.lnrn[2] 
            +'para Acelerar \n')
        else:                                                                             #Se não, imprime apenas Continuar e Melhorar
            print('Necessidade de recursos do projeto' + str(p.nome) + 'é de:'+ 
            p.lnrn[0] +'para Continuar e '+ p.lnrn[1] +'para Melhorar \n')



#20 - NECESSIDADE DE RECURSOS DE CADA ÁREA

def NecRecPa(estado_x):                                                                   #Função recebe o Estado como parâmetro

    nec0 = 0                                                                              #Variável que irá receber os valores do modo 'Continuar'
    nec1 = 0                                                                              #Variável que irá receber os valores do modo 'Melhorar'
    nec2 = 0                                                                              #Variável que irá receber os valores do modo 'Acelerar'
    lnec = []                                                                             #Lista que irá receber os valores dos modos por área 
    median = 0                                                                            #Recebe a média das listas
    for a in estado_x.A:                                                                  #Para toda área do conjunto de Áreas
        for p in estado_x.P[a]:                                                           #Para todo projeto em determinada área 
            nec0 = nec0 + p.lnrn[0]                                                       #Soma das necessidades de 'Continuar'
            nec1 = nec1 + p.lnrn[1]                                                       #Soma das necessidades de 'Melhorar'
            nec2 = nec2 + p.lnrn[2]                                                       #Soma das necessidades de 'Acelerar'

        lnec.append(nec0, nec1, nec2)                                                     #Lista de necessidades de cada modo em cada área

    median = (sum(lnec)/len(lnec))

    return median                                                                         #A função retorna uma lista contendo as necessidades para cada modo ordenada por área


#21 - NECESSIDADE DE RECURSOS DE CADA ETAPA DO FUNIL

def NecRecPe(estado_x):                                                                   #Função recebe o Estado como parâmetro

    nec0 = 0                                                                              #Variável que irá receber os valores do modo 'Continuar'
    nec1 = 0                                                                              #Variável que irá receber os valores do modo 'Melhorar'
    nec2 = 0                                                                              #Variável que irá receber os valores do modo 'Acelerar'
    lnec = []                                                                             #Lista que irá receber os valores dos modos por etapa 
    mediane = 0                                                                           #Recebe a média das listas
    for e in estado_x.E:                                                                  #Para toda área do conjunto de Etapas
        for p in estado_x.P[e]:                                                           #Para todo projeto em determinada etapa
            nec0 = nec0 + p.lnrn[0]                                                       #Soma das necessidades de 'Continuar'
            nec1 = nec1 + p.lnrn[1]                                                       #Soma das necessidades de 'Melhorar'
            nec2 = nec2 + p.lnrn[2]                                                       #Soma das necessidades de 'Acelerar'

        lnec.append(nec0, nec1, nec2)                                                     #Lista de necessidades de cada modo em cada área

    mediane = (sum(lnec)/len(lnec))

    return mediane                                                                        #A função retorna uma lista contendo as necessidades para cada modo ordenada por etapa



#22 - ORÇAMENTO TOTAL DISPONÍVEL

def OrTotal(estado_x):                                                                    #Função recebe o Estado como parâmetro

    orc = 0                                                                               #Variável que irá receber o valor do orçamento
    orc = estado_x.qn_k                                                                   #Variável recebe o orçamento daquele período

    return orc                                                                            #A função retorna o orçamento ainda disponível



#23 - QUANTIDADE DE RECURSOS MÁXIMA QUE UM PROJETO PODE ENGLOBAR

def QRecMax(estado_x):                                                                    #Função recebe o Estado como parâmetro

    costmax = 0                                                                           #Variável que recebe o custo máximo de um projeto                                             
    lcostmax = []                                                                         #Lista dos custos máximos dos projetos
    mediacm = 0                                                                           #Variável que recebe a média
    for e in estado_x.E:                                                                  #Para toda etapa do funil
        for p in estado_x.P:                                                              #Para todos os projetos nas etapas
            if(p.lnrn[2] > 0):                                                            #Se o projeto tiver o modo 'Acelerar'
                costmax = p.lnrn[2]                                                       #O custo máximo recebe o custo deste modo
                lcostmax.append(costmax)

            else:                                                                         #Se não, ele recebe o custo do modo 'Melhorar'
                costmax = p.lnrn[1]
                lcostmax.append(costmax)

    mediacm = (sum(lcostmax)/len(lcostmax))

    return mediacm                                                                        #A função retorna a média dos custos máximos de cada projeto



#24 - QUANTIDADE DE MODOS QUE UM PROJETO POSSUI POR ETAPA DO FUNIL

def QModosPe(estado_x):                                                                   #Função recebe o Estado como parâmetro

    qmodos = 0                                                                            #Variável que recebe a quantidade de modos de um projeto
    lqmodos = []                                                                          #Lista das quantidades de modos dos projetos
    mediaqm = 0                                                                           #Variável que recebe a média
    for e in estado_x.E:                                                                  #Para toda etapa do funil
        for p in estado_x.P:                                                              #Para todos os projetos nas etapas
            qmodos = len(estado_x.M.quant)                                                #Recebe a quantidade de modos do projeto
            lqmodos.append(qmodos)                                                        #A lista recebe a quantidade de modos

    mediaqm = (sum(lqmodos)/len(lqmodos))

    return mediaqm                                                                        #A função retorna a média das quantidades de modos de cada projeto



#25 - QUANTIDADE DE PROJETOS CONGELADOS NO FUNIL

def QProjCong(estado_x):                                                                  #Função recebe o Estado como parâmetro

    pcong = 0                                                                             #Variável que recebe a quantidade de projetos congelados
    pcong = len(estado_x.Pc)

    return pcong                                                                          #A função retorna os projetos congelados no funil













