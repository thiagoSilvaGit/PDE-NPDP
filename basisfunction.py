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

    mediaqp = (sum(lpe)/len(estado_x.E))

    return mediaqp                                                                        #A função retorna a lista de quantidades de projetos por etapa 'e'



#04 - QUANTIDADE DE PROJETOS POR ÁREA DO FUNIL

def QProja(estado_x):                                                                     #Função recebe o Estado como parâmetro

    contpa = 0                                                                            #Contador que irá armazenar a quantidade de projetos por área do funil
    lpa = []                                                                              #Lista que irá armazenar as quantidades de projetos por área do funil
    mediaqa = 0                                                                           #Recebe a média das listas
    lpanome = []                                                                          #Lista que irá armazenar o nome dos projetos por área do funil
    for a in range(len(estado_x.A)):                                                      #Para toda área no conjunto de Áreas
        for p in estado_x.P_a[a]:
            contpa = contpa + 1                                                           #Contador recebe o acréscimo de 1
        lpa.append(contpa)                                                                #A quantidade de projetos na área 'a' é adicionada a lista de quantidades
        contpa = 0

    mediaqa = (sum(lpa)/len(lpa))

    return mediaqa                                                                        #A função retorna a lista de quantidades de projetos por área 'a'



#05 - QUANTIDADE DE PROJETOS DE CADA ÁREA POR ETAPA DO FUNIL

def QProjae(estado_x):                                                                    #Função recebe o Estado como parâmetro

    contpae = 0                                                                           #Contador que irá armazenar a quantidade de projetos em cada área por etapa do funil
    lpaenome = []                                                                         #Lista que irá armazenar os projetos de uma área por etapa do funil
    lpae = []                                                                             #Lista que irá armazenar as quantidades de proejtos das áreas por etapa do funil
    mediaae = 0                                                                           #Recebe a média das listas
    for e in estado_x.E:                                                                  #Para todo estado no conjunto de Estados                                                             
        for a in range(len(estado_x.A)):                                                              #Para toda área no conjunto de Áreas
            for p in estado_x.P_a[a]:                                                     #Para todo projeto no conjunto de Projetos por Área
                contpae = contpae + 1                                                     #Contador recebe o acréscimo de mais 1
            lpae.append(contpae)                                                          #Lista de quantidades recebe o contador
            contpae = 0

    mediaae = (sum(lpae)/len(lpae))

    return mediaae                                                                        #A função retorna a lista com as quantidades




#06 - QUANTIDADE DE PROJETOS DIVISÍVEIS

def QProjDiv(estado_x):                                                                   #Função recebe o Estado como parâmetro

    lpdiv = []                                                                            #Lista vazia que irá armazenar os projetos que são divisíveis
    contpdiv = 0                                                                          #Contador que irá armazenar a quantidade de projetos divisíveis
    for p in estado_x.P:                                                                  #Para todos os projetos no conjunto de projetos 'P'
        if( p.div == 1):                                                                 #Se, vdiv for igual a 1, significa que o projeto é divisível
            lpdiv.append(p)                                                               #A lista recebe o projeto em questão
            contpdiv = contpdiv + 1                                                       #Acréscimo de 1 no contador

    return contpdiv                                                                       #A função retorna o contador com a quantidade total de projetos em P capazes de serem divididos



#07 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ÁREA

def QProjDiva(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lpdiva = []                                                                           #Lista para armazenar as quantidades de projetos divisíveis por área      
    lpdivanome = []                                                                       #Lista para armazenar os projetos divisíveis por área
    contpdiva = 0                                                                         #Contador dos projetos divisíveis por área
    mediada = 0                                                                           #Recebe a média das listas
    for a in range(len(estado_x.A)):                                                                  #Para toda área do conjunto de Áreas
        for p in estado_x.P_a[a]:                                                         #Para todo projeto na área 'a'
            if( p.div == 1):                                                             #Se ele for divisível
                lpdivanome.append(p)                                                      #Entra na lista 
                contpdiva = contpdiva + 1                                                 #Acréscimo de 1 no contador
        lpdiva.append(contpdiva)                                                          #A lista de quantidades recebe contpdiva
        contpdiva = 0


    mediada = (sum(lpdiva)/len(lpdiva))

    return mediada                                                                        #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



#08 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ETAPA DO FUNIL

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



#09 - QUANTIDADE DE PROJETOS NÃO-DIVISÍVEIS

def QProjnDiv(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lpndiv = []                                                                           #Lista vazia que irá armazenar os projetos que não são divisíveis
    contpndiv = 0                                                                         #Contador que irá armazenar a quantidade de projetos não divisíveis
    lpdiv = []
    for p in estado_x.P:                                                                  #Para todos os projetos no conjunto de projetos 'P'
        if( p.div != 1):                                                                 #Se, vdiv for diferente de 1, significa que o projeto não é divisível
            lpdiv.append(p)                                                               #A lista recebe o projeto em questão
            contpndiv = contpndiv + 1                                                       #Acréscimo de 1 no contador
	

    return contpndiv                                                                      #A função retorna o contador com a quantidade total de projetos em P não divisíveis



#10 - TEMPO DE CONGELAMENTO TOTAL DE CADA PROJETO

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



#11 - TEMPO DE CONGELAMENTO RESIDUAL DE CADA PROJETO

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



#12 - NECESSIDADE DE RECURSOS DE CADA PROJETO

def NecRecP(estado_x):                                                                    #Função recebe o Estado como parâmetro


    a = 0
    lnect = []
    mediant = 0
    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos 
        a = a + p.modos[p.etapa-1][0].nrn
        lnect.append(a)
    
    mediant = (sum(lnect)/len(lnect))
    return mediant



#13 - NECESSIDADE DE RECURSOS DE CADA ÁREA 

def NecRecPa(estado_x):                                                                   #Função recebe o Estado como parâmetro

    a = 0
    lnect = []
    mediant = 0
    for a in range(len(estado_x.A)):  
        for p in estado_x.P_a[a]:                                                               
            a = a + p.modos[p.etapa-1][0].nrn
            lnect.append(a)
    
        mediant = (sum(lnect)/len(lnect))
    return mediant


#14 - NECESSIDADE DE RECURSOS DE CADA ETAPA DO FUNIL

def NecRecPe(estado_x):                                                                   #Função recebe o Estado como parâmetro

    a = 0
    lnect = []
    mediant = 0
    for e in estado_x.E:  
        for p in estado_x.P_e[e-1]:                                                               
            a = a + p.modos[p.etapa-1][0].nrn
            lnect.append(a)
    
        mediant = (sum(lnect)/len(lnect))
    return mediant



#15 - ORÇAMENTO TOTAL DISPONÍVEL

def OrTotal(estado_x):                                                                    #Função recebe o Estado como parâmetro

    orc = 0                                                                               #Variável que irá receber o valor do orçamento
    a = 0
    for p in estado_x.P:
        a = a + p.modos[p.etapa-1][0].nrn
        orc = estado_x.qn_k - a                                                                #Variável recebe o orçamento daquele período

    return orc                                                                            #A função retorna o orçamento ainda disponível



#16 - QUANTIDADE DE RECURSOS MÁXIMA QUE UM PROJETO PODE ENGLOBAR

def QRecMax(estado_x):                                                                    #Função recebe o Estado como parâmetro

    costmax = 0                                                                           #Variável que recebe o custo máximo de um projeto                                             
    lcostmax = []                                                                         #Lista dos custos máximos dos projetos
    mediacm = 0                                                                           #Variável que recebe a média
    for e in estado_x.E:                                                                  #Para toda etapa do funil
        for p in estado_x.P:                                                              #Para todos os projetos nas etapas
            costmax = p.modos[p.etapa-1][0].nrn
            lcostmax.append(costmax)

    mediacm = (sum(lcostmax)/len(lcostmax))

    return mediacm                                                                        #A função retorna a média dos custos máximos de cada projeto



#17 - QUANTIDADE DE MODOS QUE UM PROJETO POSSUI

def QModosP(estado_x):                                                                    #Função recebe o Estado como parâmetro

    a = 0                                                                                 #Variável que recebe a quantidade de modos de um projeto
    cont = 0                                                                              #Lista das quantidades de modos dos projetos
    media = 0                                                                             #Variável que recebe a média
    for p in estado_x.P:
        a = len(p.modos)
        cont = cont + 1
        media = (a/cont)

    return media



#18 - QUANTIDADE DE PROJETOS CONGELADOS NO FUNIL

def QProjCong(estado_x):                                                                  #Função recebe o Estado como parâmetro

    pcong = 0                                                                             #Variável que recebe a quantidade de projetos congelados
    pcong = len(estado_x.Pc)

    return pcong                                                                          #A função retorna os projetos congelados no funil



#19 - QUANTIDADE DE PROJETOS CONGELADOS POR ETAPA DO FUNIL

def QProjCongE(estado_x):                                                                 #Função recebe o Estado como parâmetro

    pcong = 0                                                                             #Variável que recebe a quantidade de projetos congelados por etapa do funil
    lpcong = []                                                                           #Lista que recebe os projetos congelados por etapa do funil
    mediapg = 0                                                                           #Variável que recebe a média
    for e in estado_x.E:                                                                  #Para toda etapa do funil
        pcong = len(estado_x.Pc)
        lpcong.append(pcong)

    mediapg = (sum(lpcong)/len(lpcong))

    return mediapg                                                                        #A função retorna a média da quantidade de projetos congelados por etapa do funil



#20 - QUANTIDADE DE PROJETOS CONGELADOS POR ÁREA

def QProjCongA(estado_x):                                                                 #Função recebe o Estado como parâmetro

    pcong = 0                                                                             #Variável que recebe a quantidade de projetos congelados por área
    lpcong = []                                                                           #Lista que recebe os projetos congelados por área
    mediapga = 0                                                                          #Variável que recebe a média
    for a in estado_x.A:                                                                  #Para toda área do funil
        pcong = len(estado_x.Pc)
        lpcong.append(pcong)

    mediapga = (sum(lpcong)/len(lpcong))

    return mediapga                                                                       #A função retorna a média da quantidade de projetos congelados por área



#21 - RETORNO TOTAL FINAL MÍNIMO ESPERADO POR PROJETO 

def RetMnTotalProj(estado_x):                                                               #Função recebe o Estado como parâmetro                                                                  

    retesp1 = 0                                                                            #Variável que recebe os retornos esperados
    for p in estado_x.Pl:
        retesp1 = retesp1 + p.par[1]                                                        
        

    return retesp1                                                                         #A função retorna a média dos retornos finais esperados



#22 - RETORNO TOTAL FINAL MÁXIMO ESPERADO POR PROJETO 

def RetMxTotalProj(estado_x):                                                               #Função recebe o Estado como parâmetro                                                                  

    retesp2 = 0                                                                            #Variável que recebe os retornos esperados
    for p in estado_x.Pl:
        retesp2 = retesp2 + p.par[0]                                                        
        

    return retesp2                                                                         #A função retorna a média dos retornos finais esperados



#23 - RETORNO TOTAL MÍNIMO FINAL ESPERADO POR PROJETOS DE UMA ÁREA

def RetMnTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média dos retornos esperados
    lretesp = []                                                                          #Lista que recebe os valores médios de retorno
    mediara = 0                                                                           #Variável que recebe a média
    for p in estado_x.Pl:                                                                 #Para todo projeto no conjunto de projetos lançados
        for a in range(len(estado_x.A)):                                                              #Para toda área no conjunto de Áreas
            retesp = p.par[1]                                                          #Faz-se a média do retorno máximo e mínimo esperado
            lretesp.append(retesp)

    mediara = (sum(lretesp))

    return mediara                                                                        #A função retorna a média dos retornos finais esperados



#24 - RETORNO TOTAL MÁXIMO FINAL ESPERADO POR PROJETOS DE UMA ÁREA

def RetMxTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média dos retornos esperados
    lretesp = []                                                                          #Lista que recebe os valores médios de retorno
    mediara = 0                                                                           #Variável que recebe a média
    for p in estado_x.Pl:                                                                 #Para todo projeto no conjunto de projetos lançados
        for a in range(len(estado_x.A)):                                                              #Para toda área no conjunto de Áreas
            retesp = p.par[0]                                                          #Faz-se a média do retorno máximo e mínimo esperado
            lretesp.append(retesp)

    mediara = (sum(lretesp))

    return mediara                                                                        #A função retorna a média dos retornos finais esperados



#25 - DESEMPENHO MÁXIMO ESPERADO NA EXECUÇÃO DE UM PROJETO

def DesemMxProj(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    b = 0
    cont = 0
    media = 0	
    for p in estado_x.P:                                                                         
        b = b + p.par[0] - p.modos[p.etapa-1][0].nrn
        cont = cont + 1
        media = (b/cont)		


    return media                                                                         #A função retorna a média do desempenho esperado



#26 - DESEMPENHO MÍNIMO ESPERADO NA EXECUÇÃO DE UM PROJETO

def DesemMnProj(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    b = 0
    cont = 0
    media = 0	
    for p in estado_x.P:                                                                         
        b = b + p.par[1] - p.modos[p.etapa-1][0].nrn
        cont = cont + 1
        media = (b/cont)		


    return media                                                                         #A função retorna a média do desempenho esperado



#27 - VPL MÍNIMO TOTAL DA CARTEIRA

def VPLMnTotal(estado_x):                                                                 #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    mediavpl = 0                                                                          #Variável que recebe a média
    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos lançados
        retesp = (p.par[1]/(1+sum(p.tempo)))                                              #Recebe-se o VPL
        lretesp.append(retesp)

    mediavpl = sum(lretesp)

    return mediavpl                                                                       #A função retorna o somatório do VPL de cada projeto na carteira



#28 - VPL MÁXIMO TOTAL DA CARTEIRA

def VPLMxTotal(estado_x):                                                                 #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    mediavpl = 0                                                                          #Variável que recebe a média
    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos lançados
        retesp = (p.par[0]/(1+sum(p.tempo)))                                              #Recebe-se o VPL
        lretesp.append(retesp)

    mediavpl = sum(lretesp)

    return mediavpl                                                                       #A função retorna o somatório do VPL de cada projeto na carteira



#29 - CUSTO MÍNIMO TOTAL DA CARTEIRA

def CustoMnTotal(estado_x):                                                               #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            
    lretesp = []                                                                          
    mediacmin = 0                                                                         
    for p in estado_x.Pl:                                                                 
        retesp = (p.par[1]/(1+ sum(p.tempo)))           
        lretesp.append(retesp)

    mediacmin = sum(lretesp)

    return mediacmin                                                                      #A função retorna custos mínimos da carteira



#30 - CUSTO MÁXIMO TOTAL DA CARTEIRA

def CustoMxTotal(estado_x):                                                               #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            
    lretesp = []                                                                          
    mediacmin = 0                                                                         
    for p in estado_x.Pl:                                                                 
        retesp = (p.par[0]/(1+ sum(p.tempo)))           
        lretesp.append(retesp)

    mediacmin = sum(lretesp)

    return mediacmin                                                                      #A função retorna custos mínimos da carteira



#31 - VPL TOTAL MÍNIMO DA CARTEIRA POR ÁREA

def VPLMnTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    lmediavpla = []                                                                       #Lista que recebe a média
    mediavpla = 0                                                                         #Variável que recebe a média final
    for a in range(len(estado_x.A)):                                                                  #Para toda área no conjunto de áreas
        for p in estado_x.Pl:                                                             #Para todo projeto no conjunto de projetos lançados
            retesp = (p.par[1]/(1+sum(p.tempo)))                                                    #Recebe-se o VPL
            lretesp.append(retesp)

    lmediavpla.append(sum(lretesp))
    mediavpla = (sum(lmediavpla)/len(lmediavpla))

    return mediavpla                                                                      #A função retorna a média do somatório do VPL de cada projeto na carteira por área


#32 - VPL TOTAL MÁXIMO DA CARTEIRA POR ÁREA

def VPLMxTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    lmediavpla = []                                                                       #Lista que recebe a média
    mediavpla = 0                                                                         #Variável que recebe a média final
    for a in range(len(estado_x.A)):                                                                  #Para toda área no conjunto de áreas
        for p in estado_x.Pl:                                                             #Para todo projeto no conjunto de projetos lançados
            retesp = (p.par[0]/(1+sum(p.tempo)))                                                    #Recebe-se o VPL
            lretesp.append(retesp)

    lmediavpla.append(sum(lretesp))
    mediavpla = (sum(lmediavpla)/len(lmediavpla))

    return mediavpla                                                                      #A função retorna a média do somatório do VPL de cada projeto na carteira por área


#33 - VPL TOTAL MÍNIMO DA CARTEIRA POR ETAPA DO FUNIL

def VPLMnTotalE(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    lmediavple = []                                                                       #Variável que recebe a média
    mediavple = 0                                                                         #Variável que recebe a média final
    for e in estado_x.E:                                                                  #Para toda área no conjunto de etapas
        for p in estado_x.P:                                                              #Para todo projeto no conjunto de projetos 
            retesp = (p.par[1]/(1+sum(p.tempo)))                                                    #Recebe-se o VPL
            lretesp.append(retesp)

    lmediavple.append(sum(lretesp))
    mediavple = (sum(lmediavple)/len(lmediavple))

    return mediavple                                                                      #A função retorna a média do somatório do VPL de cada projeto na carteira por etapa



#34 - VPL TOTAL MÁXIMO DA CARTEIRA POR ETAPA DO FUNIL

def VPLMxTotalE(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    lmediavple = []                                                                       #Variável que recebe a média
    mediavple = 0                                                                         #Variável que recebe a média final
    for e in estado_x.E:                                                                  #Para toda área no conjunto de etapas
        for p in estado_x.P:                                                              #Para todo projeto no conjunto de projetos 
            retesp = (p.par[0]/(1+sum(p.tempo)))                                                    #Recebe-se o VPL
            lretesp.append(retesp)

    lmediavple.append(sum(lretesp))
    mediavple = (sum(lmediavple)/len(lmediavple))

    return mediavple                                                                      #A função retorna a média do somatório do VPL de cada projeto na carteira por etapa



#35 - CUSTO MÍNIMO DOS PROJETOS CONGELADOS

def CustoMnTotalCong(estado_x):                                                           #Função recebe o Estado como parâmetro                                                                                                                                

    retesp = 0                                                                            
    lretesp = []                                                                          
    mediacmin = 0                                                                         
    for p in estado_x.Pc:                                                                 
        retesp = (p.par[1]/(1+ sum(p.tempo)))           
        lretesp.append(retesp)

    mediacmin = sum(lretesp)

    return mediacmin



#36 - CUSTO MÁXIMO DOS PROJETOS CONGELADOS

def CustoMxTotalCong(estado_x):                                                           #Função recebe o Estado como parâmetro                                                                                                                                

    retesp = 0                                                                            
    lretesp = []                                                                          
    mediacmin = 0                                                                         
    for p in estado_x.Pc:                                                                 
        retesp = (p.par[0]/(1+ sum(p.tempo)))           
        lretesp.append(retesp)

    mediacmin = sum(lretesp)

    return mediacmin	


''' Função de escrita de dados '''

def save_cabecalho(estado_x, nome_do_arq):

	listaCabecalho = ['valorSim - custoSim', 'v0','custoSim','valorSim','QProj', 'QProjNovos', 'QProje', 'Qproja', 'Qprojae', 'QProjDiv', 'QProjDiva', 'QProjDive', 'QProjnDiv', 'TCongP', 'TCongReP', 'NecRecP', 'NecRecPa', 'NecRecPe', 'OrTotal', 'QRecMax', 'QModosP', 'QProjCong', 'QProjCongE', 'QProjCongA', 'RetMnTotalProj', 'RetMxTotalProj', 'RetMnTotalA', 'RetMxTotalA', 'DesemMxProj', 'DesemMnProj', 'VPLMnTotal', 'VPLMxTotal', 'CustoMnTotal', 'CustoMxTotal', 'VPLMnTotalA', 'VPLMxTotalA', 'VPLMnTotalE', 'VPLMxTotalE', 'CustoMnTotalCong', 'CustoMxTotalCong']
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
        nfile.write('{:.2f},'.format(QProja(estado_x)))
        nfile.write('{:.2f},'.format(QProjae(estado_x)))
        nfile.write('{:.2f},'.format(QProjDiv(estado_x)))
        nfile.write('{:.2f},'.format(QProjDiva(estado_x)))
        nfile.write('{:.2f},'.format(QProjDive(estado_x)))
        nfile.write('{:.2f},'.format(QProjnDiv(estado_x)))
        nfile.write('{:.2f},'.format(TCongP(estado_x)))
        nfile.write('{:.2f},'.format(TCongReP(estado_x)))
        nfile.write('{:.2f},'.format(NecRecP(estado_x)))
        nfile.write('{:.2f},'.format(NecRecPa(estado_x)))
        nfile.write('{:.2f},'.format(NecRecPe(estado_x)))
        nfile.write('{:.2f},'.format(OrTotal(estado_x)))
        nfile.write('{:.2f},'.format(QRecMax(estado_x)))
        nfile.write('{:.2f},'.format(QModosP(estado_x)))
        nfile.write('{:.2f},'.format(QProjCong(estado_x)))
        nfile.write('{:.2f},'.format(QProjCongE(estado_x)))
        nfile.write('{:.2f},'.format(QProjCongA(estado_x)))
        nfile.write('{:.2f},'.format(RetMnTotalProj(estado_x)))
        nfile.write('{:.2f},'.format(RetMxTotalProj(estado_x)))
        nfile.write('{:.2f},'.format(RetMnTotalA(estado_x)))
        nfile.write('{:.2f},'.format(RetMxTotalA(estado_x)))
        nfile.write('{:.2f},'.format(DesemMxProj(estado_x)))	
        nfile.write('{:.2f},'.format(DesemMnProj(estado_x)))		
        nfile.write('{:.2f},'.format(VPLMnTotal(estado_x)))
        nfile.write('{:.2f},'.format(VPLMxTotal(estado_x)))			
        nfile.write('{:.2f},'.format(CustoMnTotal(estado_x)))
        nfile.write('{:.2f},'.format(CustoMxTotal(estado_x)))		
        nfile.write('{:.2f},'.format(VPLMnTotalA(estado_x)))
        nfile.write('{:.2f},'.format(VPLMxTotalA(estado_x)))	
        nfile.write('{:.2f},'.format(VPLMnTotalE(estado_x)))
        nfile.write('{:.2f},'.format(VPLMxTotalE(estado_x)))	
        nfile.write('{:.2f},'.format(CustoMnTotalCong(estado_x)))
        nfile.write('{:.2f},'.format(CustoMxTotalCong(estado_x)))		
        nfile.write('\n')

