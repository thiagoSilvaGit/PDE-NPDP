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
        for p in estado_x.P_e[e-1]:                                                         #Para todo projeto em cada estado 'e'
            contpe = contpe + 1                                                           #Contador recebe o acréscimo de 1
            lpenome.append(p)                                                             #O projeto é adicionado na lista
        lpe.append(contpe)                                                                #A quantidade de projetos no estado 'e' é adicionada a lista de quantidades
        contpe = 0

    mediaqp = (sum(lpe)/len(lpe))

    return mediaqp                                                                        #A função retorna a lista de quantidades de projetos por etapa 'e'



#04 - QUANTIDADE DE RECURSOS ALOCADOS NO FUNIL

#def QRecAloc(estado_x, Politica):                                                                   #Função recebe o Estado como parâmetro

#    qtotal = 0
#    for e in estado_x.E:                                                                  #Para todo etapa no conjunto de Etapas do funil
#        qtotal = qtotal + Politica.tn[e]                                                  #qtotal recebe os valores alocados por etapa

#    return qtotal                                                                         #A função retorna qtotal com a quantidade total de recursos alocados em todas as etapas do funil



#05 - QUANTIDADE DE RECURSOS ALOCADOS EM CADA ETAPA DO FUNIL

#def QRecAloce(estado_x):                                                                  #Função recebe o Estado como parâmetro

#    lqtotale = []                                                                         #Lista que irá armazenar as quantidades alocadas em cada etapa do funil
#    mediaqr = 0                                                                           #Recebe a média das listas
#    for e in estado_x.E:                                                                  #Para cada etapa no conjunto de Etapas do funil
#        lqtotale.append(estado_x.tn[e])                                                   #Lista recebendo os valores

#    mediaqr = (sum(lqtotale)/len(lqtotale))

#    return mediaqr                                                                        #A função retorna lqtotal que é a lista com todos os valores alocados por etapa no funil



#06 - QUANTIDADE DE PROJETOS POR ÁREA DO FUNIL

def QProja(estado_x):                                                                     #Função recebe o Estado como parâmetro

    contpa = 0                                                                            #Contador que irá armazenar a quantidade de projetos por área do funil
    lpa = []                                                                              #Lista que irá armazenar as quantidades de projetos por área do funil
    mediaqa = 0                                                                           #Recebe a média das listas
    lpanome = []                                                                          #Lista que irá armazenar o nome dos projetos por área do funil
    for a in estado_x.A:                                                                  #Para toda área no conjunto de Áreas
        for p in estado_x.P_a.index(a):                                                         #Para todo projeto em cada área 'a'
            contpe = contpe + 1                                                           #Contador recebe o acréscimo de 1
        lpa.append(contpa)                                                                #A quantidade de projetos na área 'a' é adicionada a lista de quantidades
        contpa = 0

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
            lpae.append(contpae)                                                          #Lista de quantidades recebe o contador
            contpae = 0

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
        if( p.div == 1):                                                                 #Se, vdiv for igual a 1, significa que o projeto é divisível
            lpdiv.append(p)                                                               #A lista recebe o projeto em questão
            contpdiv = contpdiv + 1                                                       #Acréscimo de 1 no contador

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


    mediada = (sum(lpdiva)/len(lpdiva))

    return mediada                                                                        #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



#12 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ETAPA DO FUNIL

def QProjDive(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lpdive = []                                                                           #Lista para armazenar as quantidades de projetos divisíveis por etapa
    lpdivenome = []                                                                       #Lista para armazenar os projetos divisíveis por etapa
    contpdive = 0                                                                         #Contador dos projetos divisíveis por etapa
    mediade = 0                                                                           #Recebe a média das listas
    for e in estado_x.E:                                                                  #Para toda etapa do conjunto de Etapas
        for p in estado_x.P_e[e-1]:                                                         #Para todo projeto na etapa 'e'
            if( p.div == 1):                                                             #Se ele for divisível
                lpdivenome.append(p)                                                      #Entra na lista
                contpdive = contpdive + 1                                                 #Acréscimo de 1 no contador

        lpdive.append(contpdive)                                                          #A lista de quantidades recebe contpdive
        contpdive = 0


    mediade = (sum(lpdive)/len(lpdive))

    return mediade                                                                        #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



#13 - QUANTIDADE DE PROJETOS NÃO-DIVISÍVEIS

def QProjnDiv(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lpndiv = []                                                                           #Lista vazia que irá armazenar os projetos que não são divisíveis
    contpndiv = 0                                                                         #Contador que irá armazenar a quantidade de projetos não divisíveis
    lpdiv = []
    for p in estado_x.P:                                                                  #Para todos os projetos no conjunto de projetos 'P'
        if( p.div != 1):                                                                 #Se, vdiv for diferente de 1, significa que o projeto não é divisível
            lpdiv.append(p)                                                               #A lista recebe o projeto em questão
            contpndiv = contpndiv + 1                                                       #Acréscimo de 1 no contador
	

    return contpndiv                                                                      #A função retorna o contador com a quantidade total de projetos em P não divisíveis



#14 - TEMPO DE CONGELAMENTO TOTAL DE CADA PROJETO

def TCongP(estado_x):                                                                     #Função recebe o Estado como parâmetro

    lpdivl = []                                                                           #Lista vazia que irá armazenar os projetos divisíveis
    ltempo = []                                                                           #Lista vazia que irá armazenar os tempos congelados de cada projeto
    mediat = 0                                                                            #Recebe a média das listas
    for p in estado_x.Pl:                                                                 #Para todo projeto lançado
        if(p.div == 1):                                                                  #Se for divisível
            lpdivl.append(p)                                                              #Lista recebe os projetos 

        ltempo.append(p.congatual)                                                        #A lista recebe os tempos de congelamento de cada projeto lançado

    mediat = (sum(ltempo))

    return mediat                                                                         #A função retorna os tempos congelados de cada projeto



#15 - TEMPO DE CONGELAMENTO RESIDUAL DE CADA PROJETO

def TCongReP(estado_x):                                                                   #Função recebe o Estado como parâmetro

    laux = []                                                                             #Lista que irá armazenar os projetos divisíveis
    residual = 0                                                                          #Variável que irá armazenar os tempos residuais
    mediare = 0                                                                           #Recebe a média das listas
    lresidual = []                                                                        #Lista que irá armazenar os tempos residuais de cada projeto
    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos
        if(p.div == 1):                                                                  #Se o projeto for divisível
            laux.append(p)                                                                #Lista armazena o projeto
            residual = p.cmax - p.congatual                                               #Residual recebe a diferença do tempo máximo e o congelamento atual
            lresidual.append(residual)                                                    #Lista armazena os tempos residuais de cada projeto

    mediare = (sum(lresidual))

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
        for p in estado_x.P_e[e-1]:                                                           #Para todo projeto no conjunto de projetos                                                                
            ltr.append(sum(estado_x.p.ltempo) - estado_x.p.Qexec)                         #A lista recebe a diferença entre o somatório total de tempos e o a quantidade executada: CRIAR ESSE PARÂMENTRO NO CÓDIGO                                                

    mediatr2 = (sum(ltr)/len(ltr))

    return mediatr2                                                                       #A função retorna os tempos residuais de cada projeto                                                                           



#18 - TEMPO RESIDUAL DE CADA PROJETO POR ÁREA

def TRePa(estado_x):                                                                      #Função recebe o Estado como parâmetro

    ltr = []                                                                              #Lista que irá armazenar os tempos residuais
    mediatr3 = 0                                                                          #Recebe a média das listas
    for a in estado_x.A:                                                                  #Para toda área no conjunto de Áreas 
        for p in estado_x.P[a]:                                                           #Para todo projeto no conjunto de projetos                                                                
            ltr.append(sum(estado_x.p.ltempo) - estado_x.p.Qexec)                         #A lista recebe a diferença entre o somatório total de tempos e o a quantidade executada: CRIAR ESSE PARÂMENTRO NO CÓDIGO                                                

    mediatr3 = (sum(ltr)/len(ltr))

    return mediatr3                                                                       #A função retorna os tempos residuais de cada projeto


#19 - NECESSIDADE DE RECURSOS DE CADA PROJETO ((((((só para um tipo))))))

def NecRecP(estado_x):                                                                    #Função recebe o Estado como parâmetro

    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos 
        if (estado_x.M.quant > 2):                                                        #Se houver o modo Acelerar, imprime os três modos
            print('Necessidade de recursos do projeto' + str(p.nome) + 'é de:'+ 
            p.lnrn[0] +'para Continuar, '+ p.lnrn[1] +'para Melhorar e' + p.lnrn[2] 
            +'para Acelerar \n')
        else:                                                                             #Se não, imprime apenas Continuar e Melhorar
            print('Necessidade de recursos do projeto' + str(p.nome) + 'é de:'+ 
            p.lnrn[0] +'para Continuar e '+ p.lnrn[1] +'para Melhorar \n')



#20 - NECESSIDADE DE RECURSOS DE CADA ÁREA ((((minimo só pro continuar))))

def NecRecPa(estado_x):                                                                   #Função recebe o Estado como parâmetro

    nec0 = 0                                                                              #Variável que irá receber os valores do modo 'Continuar'
    nec1 = 0                                                                              #Variável que irá receber os valores do modo 'Melhorar'
    nec2 = 0                                                                              #Variável que irá receber os valores do modo 'Acelerar'
    lnec = []                                                                             #Lista que irá receber os valores dos modos por área 
    median = 0                                                                            #Recebe a média das listas
    for a in estado_x.A:                                                                  #Para toda área do conjunto de Áreas
        for p in estado_x.P_a[a]:                                                           #Para todo projeto em determinada área 
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
        for p in estado_x.P_e[e-1]:                                                           #Para todo projeto em determinada etapa
            nec0 = nec0 + p.lnrn[0]                                                       #Soma das necessidades de 'Continuar'
            nec1 = nec1 + p.lnrn[1]                                                       #Soma das necessidades de 'Melhorar'
            nec2 = nec2 + p.lnrn[2]                                                       #Soma das necessidades de 'Acelerar'

        lnec.append(nec0)
        lnec.append(nec1)
        lnec.append(nec2)

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



#26 - QUANTIDADE DE PROJETOS CONGELADOS POR ETAPA DO FUNIL

def QProjCongE(estado_x):                                                                 #Função recebe o Estado como parâmetro

    pcong = 0                                                                             #Variável que recebe a quantidade de projetos congelados por etapa do funil
    lpcong = []                                                                           #Lista que recebe os projetos congelados por etapa do funil
    mediapg = 0                                                                           #Variável que recebe a média
    for e in estado_x.E:                                                                  #Para toda etapa do funil
        pcong = len(estado_x.Pc)
        lpcong.append(pcong)

    mediapg = (sum(lpcong)/len(lpcong))

    return mediapg                                                                        #A função retorna a média da quantidade de projetos congelados por etapa do funil



#27 - QUANTIDADE DE PROJETOS CONGELADOS POR ÁREA

def QProjCongA(estado_x):                                                                 #Função recebe o Estado como parâmetro

    pcong = 0                                                                             #Variável que recebe a quantidade de projetos congelados por área
    lpcong = []                                                                           #Lista que recebe os projetos congelados por área
    mediapga = 0                                                                          #Variável que recebe a média
    for a in estado_x.A:                                                                  #Para toda área do funil
        pcong = len(estado_x.Pc)
        lpcong.append(pcong)

    mediapga = (sum(lpcong)/len(lpcong))

    return mediapga                                                                       #A função retorna a média da quantidade de projetos congelados por área



#28 - RETORNO TOTAL FINAL ESPERADO POR PROJETO (((olhar a .par 0 mx 1 mn - valorLan(self,t) t = sum(p.tempo)))))RET ESP ((((POSSO FAZER MAIS UMA COM TODOS OS PROJETOS))))

def RetTotalProj(estado_x):                                                               #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média dos retornos esperados
    for p in estado_x.Pl:
        retesp = retesp + (p.Mx + p.mn)/2                                                              #Faz-se a média do retorno máximo e mínimo esperado por projeto
        

    return retesp                                                                         #A função retorna a média dos retornos finais esperados



#29 - RETORNO TOTAL FINAL ESPERADO POR PROJETOS DE UMA ÁREA

def RetTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média dos retornos esperados
    lretesp = []                                                                          #Lista que recebe os valores médios de retorno
    mediara = 0                                                                           #Variável que recebe a média
    for p in estado_x.Pl:                                                                 #Para todo projeto no conjunto de projetos lançados
        for a in estado_x.A:                                                              #Para toda área no conjunto de Áreas
            retesp = (p.Mx + p.mn)/2                                    #Faz-se a média do retorno máximo e mínimo esperado
            lretesp.append(retesp)

    mediara = (sum(lretesp))

    return mediara                                                                        #A função retorna a média dos retornos finais esperados



#30 - RETORNO TOTAL FINAL ESPERADO

def RetTotal(estado_x):                                                                   #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média dos retornos esperados
    lretesp = []                                                                          #Lista que recebe os valores médios de retorno
    mediar = 0                                                                            #Variável que recebe a média
    for p in estado_x.Pl:                                                                 #Para todo projeto no conjunto de projetos lançados
        retesp = (p.Mx + p.mn)/2                                        #Faz-se a média do retorno máximo e mínimo esperado
        lretesp.append(retesp)

    mediar = sum(lretesp)

    return mediar                                                                         #A função retorna a média dos retornos finais esperados



#31 - DESEMPENHO ESPERADO NA EXECUÇÃO DE UM PROJETO

def DesemProj(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média do desempenho esperado
    retesp = [(p.Mx + p.mn)/2 - estado_x.lnrn]                          #Faz-se a média do retorno máximo e mínimo esperado por projeto e subtrai do custo de execução


    return retesp                                                                         #A função retorna a média do desempenho esperado



#32 - DESEMPENHO ESPERADO NA EXECUÇÃO DE UM PROJETO DE UMA DETERMINADA ÁREA

def DesemProjA(estado_x):                                                                 #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média do desempenho esperado
    lretesp = []                                                                          #Lista que recebe os valores médios do desempenho
    mediarda = 0                                                                          #Variável que recebe a média
    for p in estado_x.Pl:                                                                 #Para todo projeto no conjunto de projetos lançados
        for a in estado_x.A:                                                              #Para toda área no conjunto de Áreas
            retesp = [(estado_x.p.Mx + estado_x.p.mn)/2 - estado_x.lnrn]                  #Faz-se a média do retorno máximo e mínimo esperado por projeto e subtrai do custo de execução
            lretesp.append(retesp)

    mediarda = (sum(lretesp)/len(lretesp))

    return mediarda                                                                       #A função retorna a média do desempenho final por área



#33 - DESEMPENHO ESPERADO NA EXECUÇÃO DE UM PROJETO POR ETAPA DO FUNIL

def DesemProjE(estado_x):                                                                 #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média do desempenho esperado
    lretesp = []                                                                          #Lista que recebe os valores médios do desempenho
    mediarde = 0                                                                          #Variável que recebe a média
    for p in estado_x.Pl:                                                                 #Para todo projeto no conjunto de projetos lançados
        for e in estado_x.E:                                                              #Para toda área no conjunto de etapas od funil
            retesp = [(estado_x.p.Mx + estado_x.p.mn)/2 - estado_x.lnrn]                  #Faz-se a média do retorno máximo e mínimo esperado por projeto e subtrai do custo de execução
            lretesp.append(retesp)

    mediarde = (sum(lretesp)/len(lretesp))

    return mediarde                                                                       #A função retorna a média do desempenho final por etapa do funil



#34 - VPL TOTAL DA CARTEIRA *******nova 28 (dividir por 1 + a taxa ^tres))))) A CADA SOMA DIF 34 e 28

def VPLTotal(estado_x):                                                                   #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    mediavpl = 0                                                                          #Variável que recebe a média
    for p in estado_x.Pl:                                                                 #Para todo projeto no conjunto de projetos lançados
        retesp = p.vplMax                                                          #Recebe-se o VPL
        lretesp.append(retesp)

    mediavpl = sum(lretesp)

    return mediavpl                                                                       #A função retorna o somatório do VPL de cada projeto na carteira



#35 - CUSTO MÍNIMO TOTAL DA CARTEIRA

def CustoMinTotal(estado_x):                                                              #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o Custo do modo 'Continuar'
    lretesp = []                                                                          #Lista que recebe os valores dos custos
    mediacmin = 0                                                                         #Variável que recebe a média
    for p in estado_x.Pl:                                                                 #Para todo projeto no conjunto de projetos lançados
        retesp = estado_x.p.lnrn[0]                                                       #Recebe-se o custo do modo 'Continuar' de cada projeto da carteira
        lretesp.append(retesp)

    mediacmin = sum(lretesp)

    return mediacmin                                                                      #A função retorna o somatório dos custos mínimos da carteira



#40 - TEMPO ESPERADO ATÉ O PRÓXIMO LANÇAMENTO

def TempoEspProxLan(estado_x):

    aux = 0                                                                               #Variável que irá receber o tempo residual
    param = 0                                                                             #Variável que irá retornar o menor tempo residual
    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos
        aux = sum(estado_x.p.ltempo) - estado_x.p.Qexec                                   #Aux recebe a diferença entre o somatório total de tempos e o a quantidade executada: CRIAR ESSE PARÂMENTRO NO CÓDIGO
        if(estado_x.P[0]):                                                                #Se for o primeiro projeto, guarda-se o valor
            param = aux
        else:
            if(aux < param):                                                              #Se não for, apenas se for menor que o primeiro, substitui-se o valor
                param = aux

    return param                                                                          #A função retorna o tempo até o próximo lançamento



#42 - VPL TOTAL DA CARTEIRA POR ÁREA

def VPLTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    lmediavpla = []                                                                       #Lista que recebe a média
    mediavpla = 0                                                                         #Variável que recebe a média final
    for a in estado_x.A:                                                                  #Para toda área no conjunto de áreas
        for p in estado_x.Pl:                                                             #Para todo projeto no conjunto de projetos lançados
            retesp = estado_x.p.vplMax                                                    #Recebe-se o VPL
            lretesp.append(retesp)

    lmediavpla.append(sum(lretesp))
    mediavpla = (sum(lmediavpla)/len(lmediavpla))

    return mediavpla                                                                      #A função retorna a média do somatório do VPL de cada projeto na carteira por área



#43 - VPL TOTAL DA CARTEIRA POR ETAPA DO FUNIL

def VPLTotalE(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    lmediavple = []                                                                       #Variável que recebe a média
    mediavple = 0                                                                         #Variável que recebe a média final
    for e in estado_x.E:                                                                  #Para toda área no conjunto de etapas
        for p in estado_x.P:                                                              #Para todo projeto no conjunto de projetos 
            retesp = estado_x.p.vplMax                                                    #Recebe-se o VPL
            lretesp.append(retesp)

    lmediavple.append(sum(lretesp))
    mediavple = (sum(lmediavple)/len(lmediavple))

    return mediavple                                                                      #A função retorna a média do somatório do VPL de cada projeto na carteira por etapa



#44 - CUSTO MÍNIMO TOTAL DA CARTEIRA POR ÁREA

def CustoMinTotalA(estado_x):                                                             #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o Custo do modo 'Continuar'
    lretesp = []                                                                          #Lista que recebe os valores dos custos
    mediacmina = 0                                                                        #Variável que recebe a média
    lmediacmina = []                                                                      #Lista que recebe a média dos custos
    for a in estado_x.A:                                                                  #Para toda área no conjunto de áreas
        for p in estado_x.Pl:                                                             #Para todo projeto no conjunto de projetos lançados
            retesp = estado_x.p.lnrn[0]                                                   #Recebe-se o custo do modo 'Continuar' de cada projeto da carteira
            lretesp.append(retesp)

    lmediacmina.append(sum(lretesp))
    mediacmina = (sum(lmediacmina)/len(lmediacmina))

    return mediacmina                                                                     #A função retorna a média dos custos mínimos 



#45 - CUSTO MÍNIMO TOTAL DA CARTEIRA POR ETAPA DO FUNIL

def CustoMinTotalE(estado_x):                                                             #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o Custo do modo 'Continuar'
    lretesp = []                                                                          #Lista que recebe os valores dos custos
    mediacmine = 0                                                                        #Variável que recebe a média
    lmediacmine = []                                                                      #Lista que recebe a média dos custos
    for e in estado_x.E:                                                                  #Para toda etapa 
        for p in estado_x.P:                                                              #Para todo projeto no conjunto de projetos lançados
            retesp = estado_x.p.lnrn[0]                                                   #Recebe-se o custo do modo 'Continuar' de cada projeto da carteira
            lretesp.append(retesp)

    lmediacmine.append(sum(lretesp))
    mediacmine = (sum(lmediacmine)/len(lmediacmine))

    return mediacmine                                                                     #A função retorna a média dos custos mínimos 



#47 - CUSTO MÍNIMO DOS PROJETOS CONGELADOS

def CustoMinTotalCong(estado_x):                                                          #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o Custo do modo 'Continuar'
    lretesp = []                                                                          #Lista que recebe os valores dos custos
    mediacminc = 0                                                                        #Variável que recebe a média
    for p in estado_x.Pc:                                                                 #Para todo projeto no conjunto de projetos congelados
        retesp = estado_x.p.lnrn[0]                                                       #Recebe-se o custo do modo 'Continuar' de cada projeto da carteira
        lretesp.append(retesp)

    mediacminc = sum(lretesp)

    return mediacminc                                                                     #A função retorna o somatório dos custos mínimos da carteira dos projetos congelados


''' Função de escrita de dados '''

def save_cabecalho(estado_x, nome_do_arq):

	listaCabecalho = ['valorSim - custoSim', 'v0','custoSim','valorSim','QProj', 'QProjNovos', 'QProje', 'QProjDiv', 'QProjDive', 'QProjnDiv', 'TCongP', 'TCongReP', 'OrTotal', 'QProjCong', 'QProjCongE', 'QProjCongA']
	with open(nome_do_arq, 'w') as nfile:
		for l in listaCabecalho:
			nfile.write('{:s},'.format(l))
		nfile.write('\n')

def save_data(estado_x, listaCusto, nome_do_arq):

    with open(nome_do_arq, 'a') as nfile:
        for v in listaCusto:
            nfile.write('{:.2f},'.format(v))
        nfile.write('{:.2f},'.format(QProj(estado_x))) # colocar a apartir daqui todas as outras funções
        nfile.write('{:.2f},'.format(QProjNovos(estado_x)))
        nfile.write('{:.2f},'.format(QProje(estado_x)))
#        nfile.write('{:.2f},'.format(QRecAloc(estado_x, Politica)))
#        nfile.write('{:.2f},'.format(QRecAloce(estado_x)))
#        nfile.write('{:.2f},'.format(QProja(estado_x)))
#        nfile.write('{:.2f},'.format(QReca(estado_x)))
#        nfile.write('{:.2f},'.format(QProjae(estado_x)))
#        nfile.write('{:.2f},'.format(QRecae(estado_x)))
        nfile.write('{:.2f},'.format(QProjDiv(estado_x)))
#        nfile.write('{:.2f},'.format(QProjDiva(estado_x)))
        nfile.write('{:.2f},'.format(QProjDive(estado_x)))
        nfile.write('{:.2f},'.format(QProjnDiv(estado_x)))
        nfile.write('{:.2f},'.format(TCongP(estado_x)))
        nfile.write('{:.2f},'.format(TCongReP(estado_x)))
#        nfile.write('{:.2f},'.format(TReP(estado_x)))
#        nfile.write('{:.2f},'.format(TRePe(estado_x)))
#        nfile.write('{:.2f},'.format(TRePa(estado_x)))
#        nfile.write('{:.2f},'.format(NecRecP(estado_x)))
#        nfile.write('{:.2f},'.format(NecRecPa(estado_x)))
#        nfile.write('{:.2f},'.format(NecRecPe(estado_x)))
        nfile.write('{:.2f},'.format(OrTotal(estado_x)))
#        nfile.write('{:.2f},'.format(QRecMax(estado_x)))
#        nfile.write('{:.2f},'.format(QModosPe(estado_x)))
        nfile.write('{:.2f},'.format(QProjCong(estado_x)))
        nfile.write('{:.2f},'.format(QProjCongE(estado_x)))
        nfile.write('{:.2f},'.format(QProjCongA(estado_x)))
#        nfile.write('{:.2f},'.format(RetTotalProj(estado_x)))
#        nfile.write('{:.2f},'.format(RetTotalA(estado_x)))
#        nfile.write('{:.2f},'.format(RetTotal(estado_x)))
#        nfile.write('{:.2f},'.format(DesemProj(estado_x)))	
#        nfile.write('{:.2f},'.format(DesemProjA(estado_x)))	
#        nfile.write('{:.2f},'.format(DesemProjE(estado_x)))	
#        nfile.write('{:.2f},'.format(VPLTotal(estado_x)))	
#        nfile.write('{:.2f},'.format(CustoMinTotal(estado_x)))	
#        nfile.write('{:.2f},'.format(TempoEspProxLan(estado_x)))	
#        nfile.write('{:.2f},'.format(VPLTotalA(estado_x)))	
#        nfile.write('{:.2f},'.format(VPLTotalE(estado_x)))	
#        nfile.write('{:.2f},'.format(CustoMinTotalA(estado_x)))	
#        nfile.write('{:.2f},'.format(CustoMinTotalE(estado_x)))	
#        nfile.write('{:.2f},'.format(CustoMinTotalCong(estado_x)))			
        nfile.write('\n')

