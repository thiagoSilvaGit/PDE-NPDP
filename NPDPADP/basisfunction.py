# -*- coding: utf-8 -*-
#from cStringIO import StringIO
from gurobipy import *

def switch_bf(argument):
    switcher = {
        'QTPF': QTPF,
        'NTRP': NTRP,
        'QPD': QPD,
        'QPND': QPND,
        'QPC': QPC,
        'TRC': TRC,
        'RFMN': RFMN,
        'RFMX': RFMX,
        'NMRPC': NMRPC,
        'VPLLAN': VPLLAN,
        'VPLE': VPLE,
        'RFE': RFE

    }

    obj = switcher.get(argument, lambda *args: "Invalid Basis Function")
    return obj()



class BF:
    def Calc_phi(self,estado_x):
        return 0
    def Restr(self, estado_x,lvar):
        return 0
class RFE(BF):
    #Retorno final esperado
    #Contabiliza o Somatório dos projetos no funil, levando em conta o retorno esperado com o desempenho atual
    def Calc_phi(self, estado_x):
        return self.RFE(estado_x)

    def RFE(self, estado_x):  # Função recebe o Estado como parâmetro
        vplesp = 0                                                                            #Variável que recebe os retornos esperados
        for p in estado_x.P:
            etime  = p.CalcTimeEsp()
            vlan = p.vplLan_esp(estado_x.estagio + etime, estado_x.tx)
            vplesp = vplesp + vlan
        return vplesp


    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp =0
        for p in estado_x.P:
            etime = p.CalcTimeEsp()
            for mod in range(len(p.modos[p.etapa - 1])):
                etime2 = etime  -  p.modos[p.etapa - 1][mod].deltat
                vlan = p.vplLan_esp(estado_x.estagio + etime2, estado_x.tx,p.modos[p.etapa - 1][mod].deltap)
                exp = exp + vlan*w[estado_x.P.index(p)][mod]
                if p in estado_x.Pc:
                    vlan = p.vplLan_esp(estado_x.estagio + etime, estado_x.tx)
                    exp = exp + vlan*f[estado_x.Pc.index(p)]
        return exp

class VPLE(BF):
    # VPL total esperado da carteira
    # Contabiliza o Somatório do VPL individual de cada projeto lançado considerando o desempenho atual
    def Calc_phi(self, estado_x):
        return self.VPLE(estado_x)

    def VPLE(self, estado_x):  # Função recebe o Estado como parâmetro
        vplesp = 0                                                                            #Variável que recebe os retornos esperados
        for p in estado_x.P:
            etime  = p.CalcTimeEsp()
            vlan = p.vplLan_esp(estado_x.estagio + etime, estado_x.tx)
            vplesp = vplesp + vlan - p.getMinCostToGo(p.etapa-1)
        return vplesp


    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp =0
        for p in estado_x.P:
            etime = p.CalcTimeEsp()
            for mod in range(len(p.modos[p.etapa - 1])):
                etime2 = etime  -  p.modos[p.etapa - 1][mod].deltat
                ctg = p.modos[p.etapa - 1][mod].nrn + p.getMinCostToGo(p.etapa-1, p.modos[p.etapa - 1][mod].deltat)
                vlan = p.vplLan_esp(estado_x.estagio + etime2, estado_x.tx,p.modos[p.etapa - 1][mod].deltap)
                vpl = vlan - ctg
                exp = exp + vpl*w[estado_x.P.index(p)][mod]
                if p in estado_x.Pc:
                    ctg = p.getMinCostToGo(p.etapa-1)
                    vlan = p.vplLan_esp(estado_x.estagio + etime, estado_x.tx)
                    vpl = vlan - ctg
                    exp = exp + vpl*f[estado_x.Pc.index(p)]
        return exp


class VPLLAN(BF):
    # VPL  de lançamento
    # Contabiliza o Somatório do VPL individual de cada projeto lançado
    def Calc_phi(self, estado_x):
        return self.VPLLAN(estado_x)

    def VPLLAN(self, estado_x):  # Função recebe o Estado como parâmetro
        vplesp = 0                                                                            #Variável que recebe os retornos esperados
        for p in estado_x.Pl:
            vplesp = vplesp + p.valorLan(estado_x.estagio+1) - p.getMinCostToGo(p.etapa-1,p.tempo[p.etapa-1]-1)
        return vplesp


    def Restr(self, estado_x, lvar):
        w = lvar[0]
        pPL1 = [p for p in estado_x.P if (p.etapa == len(p.tempo)) & (p.tempo[p.etapa-1]==2)]
        pPL2 = [p for p in estado_x.P if (p.etapa == len(p.tempo)-1) & (p.tempo[p.etapa-2]==1) & ( p.tempo[p.etapa-1]== 1)]
        pPL = pPL1 + pPL2
        exp = 0
        for p in pPL:
            ctg = p.getMinCostToGo(p.etapa-1, p.tempo[len(p.tempo) - 1] - 1)
            exp = exp +  quicksum((p.valorLan(estado_x.estagio+2) - p.modos[p.etapa - 1][mod].nrn - ctg)*w[estado_x.P.index(p)][mod] for mod in range(len(p.modos[p.etapa - 1])))
        return exp


class NMRPC(BF):
    # A MÉDIA SERIA NÃO LINEAR NA RESTRIÇÃO, MODIFIQUEI PARA O VALOR TOTAL
    #Necessidade média de recurso dos projetos congelados
    #Contabiliza o Somatório dos custos de todos os modos executados até os projetos terem sido congelados
    def Calc_phi(self, estado_x):
        return self.NMRPC(estado_x)

    def NMRPC(self, estado_x):  # Função recebe o Estado como parâmetro
        return sum([p.getMinCost() for p in estado_x.Pc])

    def Restr(self, estado_x, lvar):
        f = lvar[1]
        exp = quicksum(f[estado_x.Pc.index(p)]*p.getMinCost() for p in estado_x.Pc)
        return exp


class QTPF(BF):
    # CONTABILIZA Contagem de projetos no funil
    def Calc_phi(self,estado_x):
        return self.QTPF(estado_x)

    def QTPF(self,estado_x):  # Função recebe o Estado como parâmetro
        return len(estado_x.P)  # A função retorna o contador com a quantidade total de projetos no funil
    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp = quicksum(quicksum(w[estado_x.P.index(p)][mod] for mod in range(len(p.modos[p.etapa - 1]))) for p in estado_x.P if p not in estado_x.Pl) #termo 1 e 4
        exp = exp + quicksum( f[estado_x.Pc.index(p)] for p in estado_x.Pc) #termo 2
        return exp


class NTRP(BF):
    #A MÉDIA SERIA NÃO LINEAR NA RESTRIÇÃO, MODIFIQUEI PARA O VALOR TOTAL
    # CONTABILIZA A SOMA DO CUSTO TOTAL MÍNIMO NECESSÁRIO PARA LANÇAR CADA PROJETO

    def Calc_phi(self, estado_x):
        return  self.NTRP(estado_x)

    def NTRP(self,estado_x):  # Função recebe o Estado como parâmetro
        return sum([p.getMinCost() for p in estado_x.P])

    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp = quicksum(quicksum(w[estado_x.P.index(p)][mod]*p.getMinCost() for mod in range(len(p.modos[p.etapa - 1]))) for p in estado_x.P if p not in estado_x.Pl)  # termo 1 e 4
        exp = exp + quicksum(f[estado_x.Pc.index(p)]*p.getMinCost() for p in estado_x.Pc)  # termo 2
        return exp


class QPD(BF):
    # CONTABILIZA Contagem de projetos divisíveis
    def Calc_phi(self, estado_x):
        return  self.QPD(estado_x)

    def QPD(self,estado_x):

        contpdiv = 0                #Contador que irá armazenar a quantidade de projetos divisíveis
        for p in estado_x.P:            #Para todos os projetos no conjunto de projetos 'P'
            if( p.div == 1):            #Se, vdiv for igual a 1, significa que o projeto é divisível
                contpdiv = contpdiv + 1        #Acréscimo de 1 no contador

        return contpdiv                    #A função retorna o contador com a quantidade total de projetos em P capazes de serem divididos


    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp = quicksum(quicksum(w[estado_x.P.index(p)][mod] for mod in range(len(p.modos[p.etapa - 1]))) for p in estado_x.P if (p not in estado_x.Pl) and (p.div==1)) #termo 1 e 4
        exp = exp + quicksum( f[estado_x.Pc.index(p)] for p in estado_x.Pc) #termo 2
        return exp


class QPND(BF):
    # CONTABILIZA Contagem de projetos não divisíveis
    def Calc_phi(self, estado_x):
        return  self.QPND(estado_x)

    def QPND(self,estado_x):

        contpdiv = 0                #Contador que irá armazenar a quantidade de projetos não divisíveis
        for p in estado_x.P:            #Para todos os projetos no conjunto de projetos 'P'
            if( p.div != 1):            #Se, vdiv for diferente de 1, significa que o projeto não é divisível
                contpdiv = contpdiv + 1        #Acréscimo de 1 no contador

        return contpdiv                    #A função retorna o contador com a quantidade total de projetos em P não capazes de serem divididos

    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp = quicksum(quicksum(w[estado_x.P.index(p)][mod] for mod in range(len(p.modos[p.etapa - 1]))) for p in estado_x.P if (p not in estado_x.Pl) and (p.div!=1)) #termo 1 e 4
        exp = exp + quicksum( f[estado_x.Pc.index(p)] for p in estado_x.Pc) #termo 2
        return exp


class QPC(BF):
    # CONTABILIZA Contagem de projetos congelados no funil
    def Calc_phi(self,estado_x):
        return self.QPC(estado_x)

    def QPC(self,estado_x):  # Função recebe o Estado como parâmetro
        return len(estado_x.Pc)  # A função retorna o contador com a quantidade total de projetos congelados no funil
    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp = quicksum( f[estado_x.Pc.index(p)] for p in estado_x.Pc)
        return exp

class TRC(BF):
    # Calcula o somatório do tempo de congelamento residual dos projetos
    def Calc_phi(self,estado_x):
        return self.TRC(estado_x)

    def TRC(self, estado_x):                                                              #Função recebe o Estado como parâmetro

        aux = 0                                                                           #Variável que irá armazenar os tempos residuais
        for p in estado_x.P:                                                              #Para todo projeto no conjunto de projetos
            if(p.div == 1):                                                               #Se o projeto for divisível
                aux = aux + p.cmax - p.congatual                                          #Aux recebe a diferença do tempo máximo e o congelamento atual

        return aux                                                                        #A função retorna o somatório os tempos residuais de congelamento de cada projeto     

    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp = quicksum(quicksum((p.cmax - p.congatual)*w[estado_x.P.index(p)][mod] for mod in range(len(p.modos[p.etapa - 1]))) for p in estado_x.P if (p not in estado_x.Pl)) #termo 1 e 4
        exp = exp + quicksum((p.cmax - p.congatual-1)*f[estado_x.Pc.index(p)] for p in estado_x.Pc) #termo 2
        return exp


class RFMN(BF):
    # Calcula o somatório do retorno mínimo esperado dos projetos no funil
    def Calc_phi(self,estado_x):
        return self.RFMN(estado_x)

    def RFMN(self,estado_x):  # Função recebe o Estado como parâmetro
        retesp1 = 0                                                                            #Variável que recebe os retornos esperados
        for p in estado_x.P:
            retesp1 = retesp1 + p.par[1]       
        return retesp1                                                                         #A função retorna a soma dos retornos mínimos esperados

    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp = quicksum(quicksum(p.par[1]*w[estado_x.P.index(p)][mod] for mod in range(len(p.modos[p.etapa - 1]))) for p in estado_x.P if (p not in estado_x.Pl)) #termo 1 e 4
        exp = exp + quicksum( p.par[1]*f[estado_x.Pc.index(p)] for p in estado_x.Pc) #termo 2
        return exp


class RFMX(BF):
    # Calcula o somatório do retorno máximo esperado dos projetos no funil
    def Calc_phi(self,estado_x):
        return self.RFMX(estado_x)

    def RFMX(self,estado_x):  # Função recebe o Estado como parâmetro
        retesp1 = 0                                                                            #Variável que recebe os retornos esperados
        for p in estado_x.P:
            retesp1 = retesp1 + p.par[0]
        return retesp1                                                                         #A função retorna a soma dos retornos máximo esperados

    def Restr(self, estado_x, lvar):
        w = lvar[0]
        f = lvar[1]
        exp = quicksum(quicksum(p.par[0]*w[estado_x.P.index(p)][mod] for mod in range(len(p.modos[p.etapa - 1]))) for p in estado_x.P if (p not in estado_x.Pl)) #termo 1 e 4
        exp = exp + quicksum(p.par[0]*f[estado_x.Pc.index(p)] for p in estado_x.Pc) #termo 2
        return exp



''' CARACTERÍSTICAS DO ESTADO '''


#01 - QUANTIDADE TOTAL DE PROJETOS NO FUNIL

def QProj(estado_x):                                                                      #Função recebe o Estado como parâmetro

    contp = 0                                                                             #Contador que irá armazenar a quantidade de projetos total no funil
    for p in estado_x.P:                                                                  #Para todos os projetos no conjunto de projetos 'P' 
        contp = contp + 1

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



#03 - QUANTIDADE DE PROJETOS POR ÁREA

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

    mediaqa = (sum(lpa)/len(estado_x.A))

    return mediaqa                                                                        #A função retorna a lista de quantidades de projetos por área 'a'


#04 - QUANTIDADE DE PROJETOS POR ETAPA

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



#05 - QUANTIDADE DE PROJETOS DIVISÍVEIS

def QProjDiv(estado_x):                                                                   #Função recebe o Estado como parâmetro

    lpdiv = []                                                                            #Lista vazia que irá armazenar os projetos que são divisíveis
    contpdiv = 0                                                                          #Contador que irá armazenar a quantidade de projetos divisíveis
    for p in estado_x.P:                                                                  #Para todos os projetos no conjunto de projetos 'P'
        if( p.div == 1):                                                                 #Se, vdiv for igual a 1, significa que o projeto é divisível
            lpdiv.append(p)                                                               #A lista recebe o projeto em questão
            contpdiv = contpdiv + 1                                                       #Acréscimo de 1 no contador

    return contpdiv                                                                       #A função retorna o contador com a quantidade total de projetos em P capazes de serem divididos



#06 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ÁREA

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


    mediada = (sum(lpdiva)/len(estado_x.A))

    return mediada                                                                        #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



#07 - QUANTIDADE DE PROJETOS DIVISÍVEIS EM CADA ETAPA

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


    mediade = (sum(lpdive)/len(estado_x.E))

    return mediade                                                                        #A função retorna a lista lpdiva com as quantidades de projetos divisíveis por área do funil



#08 - QUANTIDADE DE PROJETOS NÃO-DIVISÍVEIS

def QProjnDiv(estado_x):                                                                  #Função recebe o Estado como parâmetro

    lpndiv = []                                                                           #Lista vazia que irá armazenar os projetos que não são divisíveis
    contpndiv = 0                                                                         #Contador que irá armazenar a quantidade de projetos não divisíveis
    lpdiv = []
    for p in estado_x.P:                                                                  #Para todos os projetos no conjunto de projetos 'P'
        if( p.div != 1):                                                                 #Se, vdiv for diferente de 1, significa que o projeto não é divisível
            lpdiv.append(p)                                                               #A lista recebe o projeto em questão
            contpndiv = contpndiv + 1                                                       #Acréscimo de 1 no contador
    

    return contpndiv                                                                      #A função retorna o contador com a quantidade total de projetos em P não divisíveis


#09 - QUANTIDADE DE PROJETOS CONGELADOS NO FUNIL

def QProjCong(estado_x):                                                                  #Função recebe o Estado como parâmetro

    pcong = 0                                                                             #Variável que recebe a quantidade de projetos congelados
    pcong = len(estado_x.Pc)

    return pcong                                                                          #A função retorna os projetos congelados no funil


#10 - QUANTIDADE DE PROJETOS CONGELADOS POR ÁREA

def QProjCongA(estado_x):                                                                 #Função recebe o Estado como parâmetro

    pcong = 0                                                                             #Variável que recebe a quantidade de projetos congelados
    pcong = len(estado_x.Pc)

    mediapg = (pcong/len(estado_x.A))

    return mediapg                                                                        #A função retorna a média da quantidade de projetos congelados por area do funil


#11 - QUANTIDADE DE PROJETOS CONGELADOS POR ETAPA

def QProjCongE(estado_x):                                                                 #Função recebe o Estado como parâmetro

    pcong = 0                                                                             #Variável que recebe a quantidade de projetos congelados
    pcong = len(estado_x.Pc)

    mediapg = (pcong/len(estado_x.E))

    return mediapg                                                                        #A função retorna a média da quantidade de projetos congelados por etapa do funil


#12 - TEMPO DE CONGELAMENTO RESIDUAL DOS PROJETOS

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



#13 - NECESSIDADE DE RECURSOS MÉDIA DE CADA PROJETO

def NecRecP(estado_x):                                                                    #Função recebe o Estado como parâmetro


    a = 0
    lnect = []
    mediant = 0
    for p in estado_x.P:                                                                  #Para todo projeto no conjunto de projetos 
        a = a + p.modos[p.etapa-1][0].nrn
        lnect.append(a)
    
    mediant = (sum(lnect)/len(lnect))
    return mediant



#14 - NECESSIDADE DE RECURSOS DE CADA ÁREA 

def NecRecPa(estado_x):                                                                   #Função recebe o Estado como parâmetro

    a = 0
    lnect = []
    mediant = 0
    for a in range(len(estado_x.A)):  
        for p in estado_x.P_a[a]:                                                               
            a = a + p.modos[p.etapa-1][0].nrn
            lnect.append(a)
    
        mediant = (sum(lnect)/len(estado_x.A))
    return mediant


#15 - NECESSIDADE DE RECURSOS DE CADA ETAPA 

def NecRecPe(estado_x):                                                                   #Função recebe o Estado como parâmetro

    a = 0
    lnect = []
    mediant = 0
    for e in estado_x.E:  
        for p in estado_x.P_e[e-1]:                                                               
            a = a + p.modos[p.etapa-1][0].nrn
            lnect.append(a)
    
        mediant = (sum(lnect)/len(estado_x.E))
    return mediant


#16 - NECESSIDADE MÉDIA DE RECURSOS DOS PROJETOS CONGELADOS

def NecRecPCong(estado_x):                                                           #Função recebe o Estado como parâmetro                                                                                                                                

    a = 0
    lnectc = []
    mediantc = 0
    for p in estado_x.Pc:                                                                  #Para todo projeto no conjunto de projetos congelados
        a = a + p.modos[p.etapa-1][0].nrn
        lnectc.append(a)
    
    mediantc = (sum(lnectc)/1 + len(lnectc))

    return mediantc



#17 - RETORNO FINAL MÍNIMO ESPERADO

def RetMnTotalProj(estado_x):                                                               #Função recebe o Estado como parâmetro                                                                  

    retesp1 = 0                                                                            #Variável que recebe os retornos esperados
    for p in estado_x.P:
        retesp1 = retesp1 + p.par[1]                                                        
        

    return retesp1                                                                         #A função retorna a média dos retornos finais esperados



#18 - RETORNO TOTAL FINAL MÁXIMO ESPERADO

def RetMxTotalProj(estado_x):                                                               #Função recebe o Estado como parâmetro                                                                  

    retesp2 = 0                                                                            #Variável que recebe os retornos esperados
    for p in estado_x.P:
        retesp2 = retesp2 + p.par[0]                                                        
        

    return retesp2                                                                         #A função retorna a média dos retornos finais esperados



#19 - RETORNO FINAL MÍNIMO ESPERADO POR ÁREA

def RetMnTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média dos retornos esperados
    lretesp = []                                                                          #Lista que recebe os valores médios de retorno
    mediara = 0                                                                           #Variável que recebe a média
    for p in estado_x.P:                                                                 #Para todo projeto no conjunto de projetos lançados
        for a in range(len(estado_x.A)):                                                              #Para toda área no conjunto de Áreas
            retesp = p.par[1]                                                          #Faz-se a média do retorno máximo e mínimo esperado
            lretesp.append(retesp)

    mediara = (sum(lretesp))

    return mediara                                                                        #A função retorna a média dos retornos finais esperados



#20 - RETORNO FINAL MÁXIMO ESPERADO POR ÁREA

def RetMxTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe a média dos retornos esperados
    lretesp = []                                                                          #Lista que recebe os valores médios de retorno
    mediara = 0                                                                           #Variável que recebe a média
    for p in estado_x.P:                                                                 #Para todo projeto no conjunto de projetos lançados
        for a in range(len(estado_x.A)):                                                              #Para toda área no conjunto de Áreas
            retesp = p.par[0]                                                          #Faz-se a média do retorno máximo e mínimo esperado
            lretesp.append(retesp)

    mediara = (sum(lretesp))

    return mediara                                                                        #A função retorna a média dos retornos finais esperados



#21 - DESEMPENHO MÁXIMO MÉDIO ESPERADO NA EXECUÇÃO DOS PROJETOS

def DesemMxProj(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    b = 0
    cont = 0
    media = 0    
    for p in estado_x.P:                                                                         
        b = b + p.par[0] - p.modos[p.etapa-1][0].nrn
        cont = cont + 1
        media = (b/cont)        


    return media                                                                         #A função retorna a média do desempenho esperado



#22 - DESEMPENHO MÍNIMO ESPERADO NA EXECUÇÃO DE UM PROJETO

def DesemMnProj(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    b = 0
    cont = 0
    media = 0    
    for p in estado_x.P:                                                                         
        b = b + p.par[1] - p.modos[p.etapa-1][0].nrn
        cont = cont + 1
        media = (b/cont)        


    return media                                                                         #A função retorna a média do desempenho esperado



#23 - VPL MÍNIMO TOTAL DA CARTEIRA

def VPLMnTotal(estado_x):                                                                 #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    mediavpl = 0                                                                          #Variável que recebe a média
    for p in estado_x.Pl:                                                                  #Para todo projeto no conjunto de projetos lançados
        retesp = (p.par[1]/(1+sum(p.tempo)))                                              #Recebe-se o VPL
        lretesp.append(retesp)

    mediavpl = sum(lretesp)

    return mediavpl                                                                       #A função retorna o somatório do VPL de cada projeto na carteira



#24 - VPL MÁXIMO TOTAL DA CARTEIRA

def VPLMxTotal(estado_x):                                                                 #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    mediavpl = 0                                                                          #Variável que recebe a média
    for p in estado_x.Pl:                                                                  #Para todo projeto no conjunto de projetos lançados
        retesp = (p.par[0]/(1+sum(p.tempo)))                                              #Recebe-se o VPL
        lretesp.append(retesp)

    mediavpl = sum(lretesp)

    return mediavpl                                                                       #A função retorna o somatório do VPL de cada projeto na carteira



#25 - VPL MÉDIO MÍNIMO POR ÁREA

def VPLMnTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    lmediavpla = []                                                                       #Lista que recebe a média
    mediavpla = 0                                                                         #Variável que recebe a média final
    for a in range(len(estado_x.A)):                                                                  #Para toda área no conjunto de áreas
        for p in estado_x.P:                                                             #Para todo projeto no conjunto de projetos lançados
            retesp = (p.par[1]/(1+sum(p.tempo)))                                                    #Recebe-se o VPL
            lretesp.append(retesp)

    lmediavpla.append(sum(lretesp))
    mediavpla = (sum(lmediavpla)/len(estado_x.A))

    return mediavpla                                                                      #A função retorna a média do somatório do VPL de cada projeto na carteira por área


#26 - VPL MÉDIO MÁXIMO POR ÁREA

def VPLMxTotalA(estado_x):                                                                  #Função recebe o Estado como parâmetro                                                                  

    retesp = 0                                                                            #Variável que recebe o VPL de cada projeto da carteira
    lretesp = []                                                                          #Lista que recebe os valores de VPL
    lmediavpla = []                                                                       #Lista que recebe a média
    mediavpla = 0                                                                         #Variável que recebe a média final
    for a in range(len(estado_x.A)):                                                                  #Para toda área no conjunto de áreas
        for p in estado_x.P:                                                             #Para todo projeto no conjunto de projetos lançados
            retesp = (p.par[0]/(1+sum(p.tempo)))                                                    #Recebe-se o VPL
            lretesp.append(retesp)

    lmediavpla.append(sum(lretesp))
    mediavpla = (sum(lmediavpla)/len(lmediavpla))

    return mediavpla                                                                      #A função retorna a média do somatório do VPL de cada projeto na carteira por área




''' Função de escrita de dados '''

def save_cabecalho(estado_x, nome_do_arq):

    listaCabecalho = ['valorSim', 'valorSim + custoSim','custoSim','QProj', 'QProjNovos', 'QProja', 'Qproje', 'QProjDiv', 'QProjDiva', 'QProjDive', 'QProjnDiv', 'QProjCong', 'QProjCongA', 'QProjCongE', 'TCongReP', 'NecRecP', 'NecRecPa', 'NecRecPe', 'NecRecPCong', 'RetMnTotalProj', 'RetMxTotalProj', 'RetMnTotalA', 'RetMxTotalA', 'DesemMxProj', 'DesemMnProj', 'VPLMnTotal', 'VPLMxTotal', 'VPLMnTotalA', 'VPLMxTotalA']
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
        nfile.write('{:.2f},'.format(QProja(estado_x)))
        nfile.write('{:.2f},'.format(QProje(estado_x)))
        nfile.write('{:.2f},'.format(QProjDiv(estado_x)))
        nfile.write('{:.2f},'.format(QProjDiva(estado_x)))
        nfile.write('{:.2f},'.format(QProjDive(estado_x)))
        nfile.write('{:.2f},'.format(QProjnDiv(estado_x)))
        nfile.write('{:.2f},'.format(QProjCong(estado_x)))
        nfile.write('{:.2f},'.format(QProjCongA(estado_x)))
        nfile.write('{:.2f},'.format(QProjCongE(estado_x)))
        nfile.write('{:.2f},'.format(TCongReP(estado_x)))
        nfile.write('{:.2f},'.format(NecRecP(estado_x)))
        nfile.write('{:.2f},'.format(NecRecPa(estado_x)))
        nfile.write('{:.2f},'.format(NecRecPe(estado_x)))
        nfile.write('{:.2f},'.format(NecRecPCong(estado_x)))
        nfile.write('{:.2f},'.format(RetMnTotalProj(estado_x)))
        nfile.write('{:.2f},'.format(RetMxTotalProj(estado_x)))
        nfile.write('{:.2f},'.format(RetMnTotalA(estado_x)))
        nfile.write('{:.2f},'.format(RetMxTotalA(estado_x)))
        nfile.write('{:.2f},'.format(DesemMxProj(estado_x)))    
        nfile.write('{:.2f},'.format(DesemMnProj(estado_x)))        
        nfile.write('{:.2f},'.format(VPLMnTotal(estado_x)))
        nfile.write('{:.2f},'.format(VPLMxTotal(estado_x)))            
        nfile.write('{:.2f},'.format(VPLMnTotalA(estado_x)))
        nfile.write('{:.2f},'.format(VPLMxTotalA(estado_x)))        
        nfile.write('\n')

def calc_ind(estado_x):
    return [QProj(estado_x), QProjNovos(estado_x), QProja(estado_x), QProje(estado_x), QProjDiv(estado_x), QProjDiva(estado_x), QProjDive(estado_x), QProjnDiv(estado_x), QProjCong(estado_x), QProjCongA(estado_x), QProjCongE(estado_x), TCongReP(estado_x), NecRecP(estado_x), NecRecPa(estado_x), NecRecPe(estado_x), NecRecPCong(estado_x), RetMnTotalProj(estado_x), RetMxTotalProj(estado_x), RetMnTotalA(estado_x), RetMxTotalA(estado_x), DesemMxProj(estado_x), DesemMnProj(estado_x), VPLMnTotal(estado_x), VPLMxTotal(estado_x), VPLMnTotalA(estado_x), VPLMxTotalA(estado_x)]  

