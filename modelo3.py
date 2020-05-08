# -*- coding: utf-8 -*-
from gurobipy import *
import math
from cStringIO import StringIO
import numpy as np
from scipy.stats import norm
import basisfunction as bf

#import xlwt
#import xlrd
#import datetime
#import operator

import matplotlib.pyplot as plt



fxsd = "esquema_entrada.xsd"


def GraficoLinha(lista):
    plt.plot( lista )
    x = np.array( range(len(lista)) )
#    plt.xticks(x, ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"] )
    plt.xlabel("Estagio")
    plt.ylabel("Valor")
    plt.show()

# Modelo


# Definicao das Classes

# Classe Problema
class Problema:
    # Classe com os parametros que definem a instancia do problema
    def __init__(self, vqCheg):
        self.qCheg = vqCheg # Quantidade maxima de chegadas por periodo
  
 
# Classe Gerador
class Gerador:

    def __init__(self, vna,vne):
        # Recebe a quantidade de areas
        self.nAreas = vna 
        # Recebe a quantidade de etapas do funil 
        self.nEtapas = vne 

    def geraAreas(self):
        # Gerando areas 
        A = []
        # Nomeando a area
        for a in range(self.nAreas):
            anome = 'A'+ str(a+1)
            A.append(anome)
        return A

    # Gerando os recursos do modelo: 200 multiplicando uma funcao aleatoria uniforme e adicionando 50
    def geraRecNRen(self):
        return 200*np.random.uniform()+50

    # Gerando as etapas do modelo
    def geraEtapas(self):
        return range(self.nEtapas)   

    # Gerando os projetos do modelo
    def geraProjeto(self,pid,Etapas,Areas,qrnr,estagio):
        # Nome dos projetos
        vnome = 'p'+str(pid)
        # Desvio padrao: Recebe uma distribuicao aleatoria uniforme
        desvp = np.random.uniform()
        # Tempo inicial = 0
        tempo = 0
        # Lista de tempos que determinado projeto gasta em cada etapa
        ltempo = []
        # Custo inicial = 0
        totalCost = 0;
        # Lista de modos que determinado projeto tem em cada etapa
        lmodos = []
        # Numero de etapas recebe o tamanho de etapas do funil 
        netapas = len(Etapas)
        # Os projetos iniciam na etapa 0
        vetapa = Etapas[0]
        # A area do projeto e determinada aleatoriamente dentro do conjunto de areas 
        varea = Areas[np.random.randint(0,len(Areas)-1)]
        
        for ie in range(netapas):
            nt = np.random.randint(1,4)
            ltempo.append(nt) 
            # Lista de tempos recebendo valor			
            tempo+= nt
        for ie in range(netapas):    
            quant = np.random.randint(1,3)
            imodo = self.geraModo(quant,desvp,tempo,qrnr)
            # As necessidades de recurso sendo atribuidas
            totalCost += imodo[0].nrn*ltempo[ie]		
            lmodos.append(imodo)

        # Os valores maximo e minimo esperado recebem um valor a partir de uma distribuicao uniforme multiplicada pelo custo total			
        mn =  (np.random.uniform()+1)*totalCost
        Mx = mn + np.random.uniform(2,10)*totalCost
        moda  = tempo -2 + np.random.randint(1,3)
        # Parametro de forma 
        pk = np.random.randint(2,4)
        vpk = ((pk-1)/pk)**(1/pk)
        # Parametro de escala
        a = moda/vpk 
        # Lista de parametros dos projetos recebe os valores
        lpar= [Mx,mn,a,pk,0,desvp]
        vdiv = np.random.binomial(1,0.5)
        #so pode haver congelamento maximo se o projeto for divisivel
        if(vdiv == 1):
            vcmax = 1 + math.floor(0.3*np.random.uniform()*tempo)
        else:
            vcmax = 0
        p1 = Projeto(lmodos, lpar, vdiv, ltempo, vcmax, varea,vetapa,vnome,estagio)
        return p1

    # Gerando os modos do modelo		
    def geraModo(self,quant,desv,tempo,qrnr):
        M=[]
        # Parametros dos modos: Probabilidades e necessidade de recursos
        prob1 = 0.8*np.random.uniform()
        prob2 = np.random.uniform(0.0,0.15)
        vdelta = np.random.uniform(1,3)*(desv/tempo)
        lnrn = 0.2*np.random.uniform()*qrnr
        vdeltat = 1

        # Sempre e criado o modo 'continuar'
        m1 = Modo(prob1,prob2,vdelta,lnrn,vdeltat,"Continuar")
        M.append(m1)
        # Se forem dois o numero de modos, cria-se o 'melhorar'
        if(quant>1):
            prob = np.random.uniform(prob1,1.0)
            vdelta1 = np.random.uniform(1,2)*vdelta
            vdeltat = 1
            lnrn1 = np.random.uniform(1,3)*lnrn
            vmean = np.random.uniform 
            m2 = Modo(prob,prob2,vdelta1,lnrn,vdeltat,"Melhorar")
            M.append(m2)
        # Se forem tres, cria-se o 'acelerar'
        if(quant>2):
            prob2 = np.random.uniform(0.0, prob2) 
            lnrn1 = np.random.uniform(1,3)*lnrn
            vdeltat1 = 2        
            m3 = Modo(prob1,prob2,vdelta1*(tempo/(tempo- (vdeltat1 - vdeltat))),lnrn1,vdeltat1,"Acelerar")
            M.append(m3)
        # Se for mais de 3, nao cria-se mais modos
        if(quant>3):
            print('Serao gerados apenas 3 modos')        
        return M

# Classe Modo
class Modo:
    def __init__(self, vprob,vprob2, vdelta, lnrn, vdeltat,vnome):
        # Nome do modo
        self.nome = vnome
        # Probabilidade de sucesso do modo
        self.prob = vprob
        # Probabilidade de atraso do modo
        self.probAtr = vprob2
        # Probabilidade de performance do modo
        self.deltap = vdelta
        # Necessidade de recursos nao renovaveis
        self.nrn = lnrn
        # Economia de estagios do modo
        self.deltat = vdeltat
        
    def imprime(self):
        print('Modos \n')
        print('Nome: '+ str(self.nome) + '\n')
        print('Probabilidade up: '+ str(self.prob) + '\n')
        print('Probabilidade atraso: '+ str(self.probAtr) + '\n')
        print('Delta: '+ str(self.deltap) + '\n')
        print('Necessidade de Recursos nao Renovaveis: '+ str(self.nrn) + '\n')
        print('Deltat: '+ str(self.deltat) + '\n')

# Classe Projeto
class Projeto:
    # Performance inicial
    performance = 0
    # Congelamento inicial
    congatual = 0
    def __init__(self, lmodo, lpar, vdiv, ltempo, vcmax, varea,vetapa,vnome,estagio):
        # nome: Nome do projeto
        self.nome = vnome
        # modo: modos que o projeto contem
        self.modos = lmodo
        # par: lista de parametros dos projetos
        self.par = lpar
        # div: se o projeto e divisivel ou nao
        self.div = vdiv
        # tempo:  lista de duracao residual para cada etapa - e atualizado pela decisao 
        self.tempo = ltempo
        # cmax: tempo maximo que o projeto pode ficar congelado
        self.cmax = vcmax
        # area: area do projeto
        self.area = varea
        # etapa: etapa que o projeto se encontra
        self.etapa= vetapa
        # instante de tempo para chegadas
        self.tCheg = estagio
    def getMinCost(self):
        cmin = 0
        for e in range(len(self.modos)):
            cmodmin=0
            for m in range(len(self.modos[e])):
                if(m==0):
                    cmodmin = self.modos[e][0].nrn
                else:
                    if(cmodmin>self.modos[e][m].nrn):
                        cmodmin = self.modos[e][m].nrn
            cmin = cmin + cmodmin*self.tempo[e] #assume que não haverá atraso
        return cmin 
    def valorLan(self,t):
        v1 =  (self.par[0] - self.par[1])*np.exp(-((t-self.tCheg)/self.par[2])**self.par[3])*(1 - norm.pdf(self.performance, self.par[4],self.par[5])) + self.par[1]
        print ('VALOR LAN :'+str(v1))
        return v1
    def valorLanPerf(self,t,perf):
        v1 =  (self.par[0] - self.par[1])*np.exp(-((t-self.tCheg)/self.par[2])**self.par[3])*(1 - norm.pdf(perf, self.par[4],self.par[5])) + self.par[1]
        print ('VALOR LAN :'+str(v1))
        return v1
    def valor(self,modo, t):
        perf1 = self.performance + self.modos[self.etapa-1][modo].deltap
        perf2 = self.performance - self.modos[self.etapa-1][modo].deltap
        v1 =  (self.par[0] - self.par[1])*np.exp(-((t-self.tCheg)/self.par[2])**self.par[3])*(1 - norm.pdf(perf1, self.par[4],self.par[5])) + self.par[1]
        v2 =  (self.par[0] - self.par[1])*np.exp(-((t-self.tCheg)/self.par[2])**self.par[3])*(1 - norm.pdf(perf2, self.par[4],self.par[5])) + self.par[1]
        vesp = self.modos[self.etapa-1][modo].prob*v1 + (1 - self.modos[self.etapa-1][modo].prob)*v2
        return vesp
    def imprime(self):
        print('Projetos \n')
        print('Nome: '+ str(self.nome) + '\n')
        print('Modos: \n')
        for lmod in self.modos:
            for mod in lmod:
                print mod.nome
        print('Parametros: '+ str(self.par) + '\n')
        print('Divisibilidade '+ str(self.div) + '\n')
        print('Tempos '+ str(self.tempo) + '\n')
        print('Congelamento Maximo '+ str(self.cmax) + '\n')
        print('Area '+ str(self.area) + '\n')
        print('Etapa '+ str(self.etapa) + '\n')
        
# Classe Estado_GCPDNP
class Estado_GCPDNP:
    # Estagio inicial = 0
    estagio = 0
    # Estado inical recebe as areas, etapas, o valor das constantes das restricoes, a quantidade de recursos disponivel e os projetos
    def __init__(self, lprojeto, vfi, vbe,vroum,vrodois, vqrn, lareas, letapas):
        self.A = lareas
        self.E = letapas
        self.P = lprojeto
        self.fi = vfi
        self.be = vbe
        self.roum = vroum
        self.rodois = vrodois
        self.qn_k = vqrn 
        self.P_a = [[p for p in self.P if p.area == a] for a in self.A]
        self.P_e = [[p for p in self.P if p.etapa == e] for e in self.E]
        self.Pc = [p for p in self.P if (p.div) & (p.congatual < p.cmax)]
        self.Pl = [p for p in self.P if (p.etapa == self.E[len(self.E)-1]) & (p.tempo[self.E.index(p.etapa)] == 1)]
        self.tCheg = 0
        
    def imprime(self):
        print('Estado \n')
        print('Estagio'+str(self.estagio)+' \n')
        print('Areas: '+ str(self.A) + '\n')
        print('Etapas: '+ str(self.E) + '\n')
        print('fi: '+ str(self.fi) + '\n')
        print('Quantidades de recurso nao renovaveis disponivel: '+ str(self.qn_k) + '\n')
        print('Projeto: \n ')
        for p in self.P:
            #p.imprime()
            print p.nome
            print('lista de tempos: '+ str(p.tempo) + '\n')
            print('Etapa: '+ str(p.etapa) + '\n')			
        print('Pc: \n ')
        for p in self.Pc:
			print p.nome
        print('Pl: \n ')
        for p in self.Pl:
            print p.nome
        print('P_a: \n ')
        for a in range(len(self.A)):
            print('Area '+ str(a) + ':\n') 		
            for p in self.P_a[a]:
                print p.nome
        print('P_e: \n ')
        for e in range(len(self.E)):
            print('Etapa '+ str(e) + ':\n') 		
            for p in self.P_e[e]:
                print p.nome
	# Recebe decisao
    def transicao(self,dec,vqMax):
        Incerteza = GeraIncerteza(self,dec,self.estagio,vqMax)
        Incerteza.geracao()

        # Passagem de estagio
        self.estagio = self.estagio+1
        newPe = Incerteza.Pe
        print 'NOVOS: '+ str(Incerteza.newP)
        # Adicionando os novos projetos na primeira etapa
        newPe[0] = newPe[0] + Incerteza.newP 
        self.P = []
        for e in range(len(self.E)):
            self.P_e[e] = newPe[e]
            self.P = self.P + newPe[e]
        self.P_a = [[p for p in self.P if p.area == a] for a in self.A]
        self.Pc = [p for p in self.P if (p.div) & (p.congatual < p.cmax)]
        self.Pl = [p for p in self.P if (p.etapa == self.E[len(self.E)-1]) & (p.tempo[self.E.index(p.etapa)] == 1)]
        return Incerteza.ValorAT

# Classe Decisao 		
class Decisao:
    def __init__(self, vy, vf, vw, vtn, vobj, vvalor):
        # Recebe o valor de y
        self.y = vy
        # Recebe o valor de w
        self.w = vw
        # Recebe o valor de f
        self.f = vf
        # Recebe a necessidade de recursos
        self.tn = vtn
        # Recebe o valor da funcao objetivo
        self.obj = vobj
        self.valor = vvalor
        # Os valores sao colocados de forma a decidir qual projeto continua, e cancelado ou congelado
        self.Abandonados = [p for p in range(len(self.y)) if self.y[p] == 1]
        self.Congelados = [p for p in range(len(self.f)) if self.f[p] == 1]
        self.Executados = [p for p in range(len(self.w)) if sum(self.w[p]) == 1]
        self.ExecModo =  [self.w[p].index(1) for p in self.Executados]

    def imprime(self):
        print('Abandonados: ' + str(self.Abandonados)+ '\n')
        print('Congelados: '+ str(self.Congelados) + '\n')
        print('Executados: '+ str(self.Executados) + '\n')
        print('Modos: '+ str(self.ExecModo) + '\n')
        
  
    
# Classe GeraIncerteza 		
class GeraIncerteza:
    def __init__(self, vEstado, vDecisao,vnEstagio,vqMax):
        # X: recebe o valor do estado
        self.X = vEstado
        # U: recebe a decisao corrente
        self.U = vDecisao
        self.Gen = Gerador(0,0)
        self.qnk = 0
        self.Pe = []
        self.newP = []
        self.t = vnEstagio
        self.qMax = vqMax
        self.ValorAT = 0 
# Calcula Valor dos custos apos a realizacao da incerteza
    def CalcValor(self):
        ret = 0
        print('self.Pe[len(self.Pe)-1]' +str(self.Pe[len(self.Pe)-1]))
        for p in self.X.Pl:
            print ('p.tempo: ' + str(p.tempo[len(self.Pe)-1]))		
            if p.tempo[len(self.Pe)-1] == 0:
                ret = ret + p.valorLan(self.X.estagio)
        return ret				
# Incerteza 1 - Retorno de mercado. Redefine os parametros M e m (lpar[0] e lpar[1])
    def geraIncertezaHuz1(self,proj):  

        # Redefine os parametros: retorno maximo e minimo esperados 
        if (proj.par[0]>0):
            nMx = max(proj.par[0] + np.random.normal(0,0.05*proj.par[0]),0.0)
        else:
            nMx = 0

        if (proj.par[1]>0):
            nmn = max(proj.par[1] + np.random.normal(0,0.05*proj.par[1]),0.0)
        else:
            nmn = 0

        if (nMx>nmn):
            proj.par[0] = nMx
            proj.par[1] = nmn
        else:
            proj.par[0] = 0
            proj.par[1] = 0
        return proj

# Incerteza 3 - performance esperada ao final do desenvolvimento
    def geraIncertezaHuz3(self,proj,modo): 
        u = np.random.uniform()
        if (u<=proj.modos[proj.etapa-1][modo].prob): 
            proj.performance = proj.performance + proj.modos[proj.etapa-1][modo].deltap
        else:
            proj.performance = proj.performance - proj.modos[proj.etapa-1][modo].deltap
        return proj

# Incerteza 4 - Exigencia de mercado. Redefine o parametro requisito esperado de mercado (lpar[4]) 
    def geraIncertezaHuz4(self,proj): 
        nperfmed = proj.par[4] + np.random.normal(0,0.25*proj.par[5])
        proj.par[4] = nperfmed
        return proj

# Incerteza 5 - Cronograma 
    def geraIncertezaHuz5(self,proj,id_dec):
        bAtr = 0	
        if id_dec == -1: # congelado
            proj.congatual = proj.congatual+1
        else:
            u = np.random.uniform()
            if (u>proj.modos[proj.etapa-1][id_dec].probAtr): 
                ntempo = proj.modos[proj.etapa-1][id_dec].deltat
            else:
                bAtr = 1
                ntempo = 0
            proj.tempo[proj.etapa-1] = proj.tempo[proj.etapa-1] - ntempo

        return [proj,bAtr]  

    def incertezaRec(self):
        ''' Gera a incerteza de recurso variando o valor corrente com um desvio normalmente distribuido 
            com media zero e desvio padrao igual a 5% do valor corrente ''' 
        self.qnk = max(self.X.qn_k + np.random.normal(0,0.05*self.X.qn_k),0.0)
    def incertezaProj(self):
        # Gera a incerteza de projetos
        nextPe = []   
        for e in self.X.E:
            nPe = nextPe
            nextPe = []
            for p in self.X.P_e[e-1]:
                pid = self.X.P.index(p)
                if (pid not in self.U.Abandonados):
                    if (pid in self.U.Congelados):  
                        newPe = p
                        [newPe,bAtr] = self.geraIncertezaHuz5(newPe,-1)
                    else:
                        modid = self.U.Executados.index(pid)   
                        mod = self.U.ExecModo[modid]
                        [newPe,bAtr] = self.geraIncertezaHuz5(p,mod)
                        if(not bAtr):
                            newPe = self.geraIncertezaHuz3(newPe,mod)
                        else:
                            print('projeto'+str(newPe.nome)+ 'ATRASOU')			
                    newPe = self.geraIncertezaHuz1(newPe)
                    newPe = self.geraIncertezaHuz4(newPe)
                    print newPe.tempo
                    print newPe.etapa
                    for modi in newPe.modos[newPe.etapa-1]:
                        idm = newPe.modos[newPe.etapa-1].index(modi)
                        if(modi.deltat>newPe.tempo[newPe.etapa-1]): 
                            del(newPe.modos[newPe.etapa-1][idm])
                    if(newPe.tempo[newPe.etapa-1]>0): #ainda nao terminou nesta etapa
                        nPe.append(newPe)
                    else: # terminou, adicionar no proximo conjunto
                        newPe.etapa = newPe.etapa +1
                        nextPe.append(newPe)
            self.Pe.append(nPe)

    def incertezaCheg(self):
        self.newP = []
        for i in range(self.qMax):
            pid = str(self.t)+'.'+str(i)
            pi = self.Gen.geraProjeto(pid,self.X.E,self.X.A,self.qnk,self.X.estagio)    
            self.newP.append(pi)
    def geracao(self):
        self.incertezaRec()
        self.incertezaProj()
        self.ValorAT = self.CalcValor()
        self.incertezaCheg() 

# Classe Politica
class Politica:

	def __init__(self,lbs,lcoef, gam):
		self.lBasis = lbs 
		self.B = eye(len(lcoef))
		self.Theta = array(lcoef)
		self.gamma = gam 

    def solver(self,estado_x):
# Modelo "m"
        m = Model("assignment")

# Variáveis do modelo
    # Variável y_p: Projeto abandonado
        y = []
        for p in range(len(estado_x.P)):
            y.append(m.addVar(vtype = GRB.BINARY, name = "y[{}]".format(estado_x.P[p].nome)))
        m.update()

    # Variável f_p: Projeto congelado 
        f = []
        for p in range(len(estado_x.P)):
            f.append(m.addVar(vtype = GRB.BINARY, name = "f[{}]". format(estado_x.P[p].nome)))
        m.update()    

    # Variável w_mp: Projeto continuado de determinado modo
        w = []
        for p in estado_x.P:
            linha = []
            for mod in p.modos[p.etapa -1]:    
                linha.append(m.addVar(vtype = GRB.BINARY, name = "w[{}][{}]".format(mod.nome,p.nome)))
            w.append(linha)
        m.update()

    # Variável tn_e: Quantidade de recurso alocado na etapa do funil
        tn = []
        for e in range(len(estado_x.E)):
            tn.append(m.addVar(vtype = GRB.CONTINUOUS, name = "tn[{}]".format(estado_x.E[e])))
        
        m.update()

    # Variável V_a: Penalização da área
        V = []
        for a in range(len(estado_x.A)):
            V.append(m.addVar(vtype = GRB.BINARY, name = "V[{}]".format(estado_x.A[a])))
        m.update()

    # Variável J_ep: Penalização do projeto
        J = []
        for e in range(len(estado_x.E)):
            linha = []
            for p in estado_x.P_e[e]:
                linha.append(m.addVar(vtype = GRB.BINARY, name = "J[{}][{}]".format(estado_x.E[e],p.nome)))
            J.append(linha)
        m.update()

    # Variável mn_a: Ativar ou desativar determinada restrição das áreas
        mn = []
        for a in range(len(estado_x.A)):
            mn.append(m.addVar(vtype = GRB.BINARY, name = "mn[{}]".format(estado_x.A[a])))
        m.update()

    # Variável Quota_a: Cota para execução dos projetos em uma área
        Quota =[]
        for a in range(len(estado_x.A)):
            Quota.append(m.addVar(vtype = GRB.CONTINUOUS, name = "Quota[{}]".format(estado_x.A[a])))

        m.update()
    # Parâmetro cmin_a: Custo mínimo para execução dos projetos em uma area
        cmin = []
        for a in range(len(estado_x.A)):
            cmina = 0
            for pa in estado_x.P_a[a]:
                cmodmin = pa.modos[pa.etapa-1][0].nrn
                for mod in range(1,len(pa.modos[pa.etapa-1])):
                    if pa.modos[pa.etapa-1][mod].nrn < cmodmin:
                        cmodmin = pa.modos[pa.etapa-1][mod].nrn
                cmina = cmina+ cmodmin
            cmin.append(cmina)      


# Função Objetivo           
        m.setObjective(quicksum((p.valor(mod,estado_x.estagio) - p.getMinCost())*w[estado_x.P.index(p)][mod] for p in estado_x.P for mod in range(len(p.modos[estado_x.E.index(p.etapa)]))) - quicksum(V[a]*estado_x.roum for a in range(len(estado_x.A)))- quicksum(J[e][idp]*estado_x.rodois for e in range(len(estado_x.E)) for idp in range(len(estado_x.P_e[e]))), GRB.MAXIMIZE)
	#
# Restrições
        
    # Restrição 1: Status dos projetos que não podem ser congelados 
        PmPc = [p for p in estado_x.P if p not in estado_x.Pc]
        for p in range(len(PmPc)):
            ip = estado_x.P.index(PmPc[p])
            m.addConstr(y[ip] + quicksum(w[ip][mod] for mod in range(len(PmPc[p].modos[estado_x.E.index(PmPc[p].etapa)]))) == 1)  
        
    # Restrição 2: Status dos projetos que podem ser congelados 
        for p in range(len(estado_x.Pc)):
            ip = estado_x.P.index(estado_x.Pc[p])        
            m.addConstr(y[ip] + f[ip] +quicksum(w[ip][mod] for mod in range(len(estado_x.Pc[p].modos[estado_x.E.index(estado_x.Pc[p].etapa)]))) == 1)        
        
    # Restrição 3: O somatório das necessidades de recursos dos projetos ativos deve ser igual a quantidade disponível por etapa
        for e in range(len(estado_x.E)):
            m.addConstr( quicksum(quicksum(w[estado_x.P.index(estado_x.P_e[e][idp])][mod]*estado_x.P_e[e][idp].modos[e][mod].nrn for mod in range(len(estado_x.P_e[e][idp].modos[e]))) for idp in range(len(estado_x.P_e[e])) ) == tn[e] )
     
    # Restrição 4: Um projeto nao poderá capturar todo o recurso disponível por etapa
        for e in range(len(estado_x.E)):
            for p in range(len(estado_x.P_e[e])):
                m.addConstr(quicksum(w[estado_x.P.index(estado_x.P_e[e][p])][mod]*estado_x.P_e[e][p].modos[e][mod].nrn for mod in range(len(estado_x.P_e[e][p].modos[e]))) <=  estado_x.fi*tn[e]+ J[e][p]*estado_x.qn_k)

    # Restrição 5a: Uma área nao poderá capturar todo o recurso disponível
        for a in range(len(estado_x.A)):
            print('a s: '+ str(a) + '\n')
            if len(estado_x.P_a[a]) > 0:
                rest=0
                for p in estado_x.P_a[a]:
                    pid = estado_x.P.index(p)
                    for mod in range(len(p.modos[p.etapa -1])):
                        rest = rest + w[pid][mod]*p.modos[p.etapa -1][mod].nrn			
                m.addConstr( rest >= Quota[a] - V[a]*estado_x.qn_k)

    # Restrição 5b
        for a in range(len(estado_x.A)):
            m.addConstr(Quota[a] >= quicksum(estado_x.be*tn[e] for e in range(len(estado_x.E))) - estado_x.qn_k*(1 - mn[a]))

    # Restrição 5c
        for a in range(len(estado_x.A)):
            m.addConstr(Quota[a] >= cmin[a] - estado_x.qn_k*(mn[a]))

     # Restrição 6: As quantidades de recurso alocadas por etapa devem ser menores ou iguais as quantidades disponiveis totais  
        m.addConstr(quicksum(tn[e] for e in range(len(estado_x.E))) <= estado_x.qn_k)
        
# Solução
        m.update()
        m.optimize()
        obj = m.objVal
        
        vy = []
        for p in range(len(estado_x.P)):
            vy.append(y[p].x)
        
        vf = []
        for p in range(len(estado_x.P)):
            vf.append(f[p].x)

        vw = []
        for p in range(len(estado_x.P)):
            vlinha = []
            ie = estado_x.E.index(estado_x.P[p].etapa)
            for mod in range(len(estado_x.P[p].modos[ie])):    
                vlinha.append(w[p][mod].x)
            vw.append(vlinha)
        print str(vw) + 'VW'
        vtn = []
        for e in range(len(estado_x.E)):
            vtn.append(tn[e].x)

        print('SOLUCAO:\n')
        for p in range(len(estado_x.P)):
            if (y[p].x>0):
                print(estado_x.P[p].nome +' foi cancelado')
            elif (f[p].x>0):
                print(estado_x.P[p].nome +' foi congelado')
            else:
                for mod in range(len(w[p])):
                    if(w[p][mod].x>0):
                        print(estado_x.P[p].nome +' foi executado com o modo '+ estado_x.P[p].modos[estado_x.E.index(estado_x.P[p].etapa)][mod].nome)
        print('RESPOSTA - PL:')
        print('faturamento: ')
        for p in estado_x.Pl:
            print p.nome
            print ('etapa: ' + str(p.etapa))
            for mod in range(len(p.modos[estado_x.E.index(p.etapa)])):
                if(w[estado_x.P.index(p)][mod].x>0.0001):
                    print('mod :' + str(mod))
                    print('w :' + str(w[estado_x.P.index(p)][mod].x))
                    print('valor :' + str(p.valor(mod,estado_x.estagio)))
                    print ('\n')
        print('Custos: ')
        for p in estado_x.P:
            print p.nome
            print ('etapa: ' + str(p.etapa))
            for mod in range(len(p.modos[estado_x.E.index(p.etapa)])):
                if(w[estado_x.P.index(p)][mod].x>0.0001):
                    print('mod :' + str(mod))
                    print('w :' + str(w[estado_x.P.index(p)][mod].x))
                    print('custo :' + str(p.modos[p.etapa -1][mod].nrn))
                    print ('\n')

				
        Valor = sum([w[estado_x.P.index(p)][mod].x*p.modos[p.etapa -1][mod].nrn for p in estado_x.P for mod in range(len(p.modos[estado_x.E.index(p.etapa)]))])
        Valor = Valor + sum([V[a].x*estado_x.roum for a in range(len(estado_x.A))])
        Valor = Valor + sum([sum([J[e][idp].x*estado_x.rodois for idp in range(len(estado_x.P_e[e]))]) for e in range(len(estado_x.E))])
	
        d = Decisao(vy, vf, vw, vtn, obj,Valor)
        return d
	def retorno(self,EstX,lpar,decisao):
        return 0
	def calc_erro_m(self,C,fgf):
		aux = npla.multi_dot(fgf*self.Theta)
		return C - aux

	def calc_denm(self,phi,fgf):
		
		aux  = np.matmul(np.matmul(fgf,self.B),np.transpose(phi_m))
		
		denm = 1.0 + aux # denominador
		if (denm>0.0)&(denm<0.00001):
			denm +=0.0001 #to avoid numerical issues; 
		else: 
			if (denm<0.0)&(denm >-0.00001): 
				denm -=0.0001; #to avoid numerical issues
	
	def UpdateB_m(self,phi_m, fgf):
		# B e theta estão na política
		denm = self.calc_demn(phi_m,fgf)
		self.B = self.B - (1/denm)*np.matmul(np.matmult(self.B,np.transpose(phi_m)),np.matmul(fgf,self.B))

	def UpdateTheta_m(self,erro,phi,fgf):
		denm = self.calc_demn(phi,fgf)
		self.Theta = self.Theta + (1/denm)*np.matmul(np.matmul(error,self.B),np.transpose(phi)) 
		

	def calc_phi(self, S, lpar):
		#basis* indicadores
		phi  = [self.lbs[i](S,lpar) for i in range(len(self.Theta))]
		a_phi = array(phi)
		return a_phi

	def calc_phiGammaPhi(self, S,Smp,lpar):
		phi_m = self.calc_phi(self, S,lpar)
		phi_mp = self.calc_phi(self, Smp,lpar)
		phiGammaPhi = phi_m - self.gamma*phi_mp # operação matricial
		return phiGammaPhi

	def updPol(self,a,Sm,Smp1,lpar):
		#recursive least squares
		#step 6d algoritmo 10.10 pag 407
		custo = self.retorno(Sm,lpar,a)
		phi_m = self.calc_phi(Sm,lpar)
		fgf =  self.calc_phiGammaPhi(Sm,Smp,lpar)

		#setp 7b alg 10.10 pag 407 - eq. 10.23 via rls
		erro = self.calcError_m(custo,fgf)
		self.UpdateTheta_m(erro,phi_m, fgf)
		self.UpdateB_m(phi_m, fgf)

	def getStatLabels():
		thetafb =['Theta_fb'+ i for i in range(len(self.lbs))]
		return thetafb

	def getStatistics():
		return self.Theta





class Politica_GulosaVPL:
    ''' Política 3: Política Gulosa

        1. Para todo o projeto, calcular o VPL esperado médio (sem considerar atraso) das seguintes situações:

            a. Continuar sempre os projetos;
            b. Melhorar depois continuar sempre os projetos;
            c. Acelerar depois continuar sempre os projetos.
        2. Selecionar o melhor VPL ($VPL_{max}$);

            a. Se $VPL_{max} \leq 0$, cancela o projeto;

               Senão:
                   i. Ranquear os projetos por VPL e fazer todos que caibam no orçamento;
                   ii. Congelar os que sobraram e, se não puder congelar, cancelar.
                   
    '''
    def __init__(self, ParPol):
        '''
           Construtor
           \par ParPol - lista com parâmetros para a politica
                       - [0]: Taxa de desconto 
           DEVE SER SOBRESCRITO
        '''  
        self.txDesc = ParPol[0]
    
    def solver(self,EstX):
        '''
           Metodo de solucao
           \par EstX - instancia da classe estado
           \return - deve retornar uma instancia da classe decisao
  
           DEVE SER SOBRESCRITO
        '''
        vy = [0 for i in range(len(EstX.P))]
        vf = [0 for i in range(len(EstX.P))]
        vtn = [0 for i in range(len(EstX.E))]
        vw = []
        for p in range(len(EstX.P)):
            vlinha = []
            ie = EstX.E.index(EstX.P[p].etapa)
            for mod in range(len(EstX.P[p].modos[ie])):    
                vlinha.append(0)
            vw.append(vlinha)

    # Parâmetro cmin_a: Custo mínimo para execução dos projetos em uma area
        cmin = []
        for a in range(len(EstX.A)):
            cmina = 0
            for pa in EstX.P_a[a]:
                cmodmin = pa.modos[pa.etapa-1][0].nrn
                for mod in range(1,len(pa.modos[pa.etapa-1])):
                    if pa.modos[pa.etapa-1][mod].nrn < cmodmin:
                        cmodmin = pa.modos[pa.etapa-1][mod].nrn
                cmina = cmina+ cmodmin
            cmin.append(cmina) 



        tupUnsorted = []
        for p in EstX.P:
            tup = self.SelectMaxModo(p)
            tupUnsorted.append(tup)
        pSorted = [p1 for _,p1 in sorted(zip(tupUnsorted,EstX.P), reverse = True)]
        tupSorted =  sorted(tupUnsorted, reverse = True)

        pCan = [EstX.P.index(pSorted[i]) for i in range(len(tupSorted))  if tupSorted[i][0]<=0.0] # guarda o índice dos projetos cancelados 
        pDec = [pSorted[i] for i in range(len(tupSorted))  if tupSorted[i][0]>0.0] # cancela os que não são viáveis

        Recdisp = EstX.qn_k
        pReal = []
        pCong = []

        vAloc = [0 for a in range(len(EstX.A))]
                  
        for pid in range(len(pDec)):
            pmodo = tupSorted[pid][1]
            petapa = pDec[pid].etapa-1
            custo = pDec[pid].modos[petapa][pmodo].nrn 
            if (custo <Recdisp):
                Recdisp = Recdisp - custo
                vtn[petapa] = vtn[petapa] + custo  
                pReal.append((EstX.P.index(pDec[pid]),pmodo)) # guarda o índice do projeto executado e seu respectivo modo de execucao
                vAloc[EstX.A.index(pDec[pid].area)] = vAloc[EstX.A.index(pDec[pid].area)]+ custo #contabiliza valor para area
            else:
                if((pDec[pid].div)&(pDec[pid].cmax>0)):
                    pCong.append(EstX.P.index(pDec[pid])) # guarda o índice do projeto congelado
                else:
                    pCan.append(EstX.P.index(pDec[pid]))  # Cancela o projeto e guarda o índice deste   

        for i in pCan:
            vy[i] = 1
        for i in pCong:
            vf[i] = 1
        for i in range(len(pReal)):
            (pid,pmodo) = pReal[i] 
            vw[pid][pmodo] = 1

        #cálculo do custo com violações
        vQ = [min(cmin[a],EstX.be*sum(vtn)) for a in range(len(EstX.A))]
        vioA = [0 for a in range(len(EstX.A))]
        for a in range(len(EstX.A)):
            if vQ[a]> vAloc[a]:
                vioA[a] = EstX.roum
        print("VioA: " + str(vioA))

        vioE = [0 for e in range(len(EstX.E))]     
        for i in range(len(pReal)):
            (pid,pmodo) = pReal[i] 
            petapa = EstX.P[pid].etapa-1
            ncusto = EstX.P[pid].modos[petapa][pmodo].nrn 
            if ncusto> vtn[petapa]*EstX.fi:
                vioE[petapa] = vioE[petapa] + EstX.rodois      
        print("VioE: " + str(vioE))     
        print('SOLUCAO:\n')
        for p in range(len(EstX.P)):
            if (vy[p]>0):
                print(EstX.P[p].nome +' foi cancelado')
            elif (vf[p]>0):
                print(EstX.P[p].nome +' foi congelado')
            else:
                for mod in range(len(vw[p])):
                    if(vw[p][mod]>0):
                        print(EstX.P[p].nome +' foi executado com o modo '+ EstX.P[p].modos[EstX.E.index(EstX.P[p].etapa)][mod].nome)
				
        Valor = sum(vtn) + sum(vioA) + sum(vioE)
        print("Gulosa - vtn: " +str(sum(vtn)))
        print("Gulosa - vioA: " +str(sum(vioA)))
        print("Gulosa - vioE: " +str(sum(vioE)))
        

 	obj=0	
        d = Decisao(vy, vf, vw, vtn, obj,Valor)
        return d


    def CalcPerfEsp(self, proj, modoinit):
        ePerf = proj.performance
        init = 1
        for e in range(proj.etapa-1, len(proj.tempo)):
            resTime = proj.tempo[e]
            i=0
            while i < resTime:
                if init:
                    ePerf = ePerf + (2*proj.modos[e][modoinit].prob -1)*proj.modos[e][modoinit].deltap #modo inicial
                    init = 0
                    i = i + proj.modos[e][modoinit].deltat
                else:
                    ePerf = ePerf + (2*proj.modos[e][0].prob -1)*proj.modos[e][0].deltap #continuar
                    i = i +  proj.modos[e][0].deltat
        return ePerf      

    def CalcTimeEsp(self, proj, modoinit):
        eTime = 0  
        eCusto = 0 # deve-se calcular o custo em termos de valor presente
        init = 1
        for e in range(proj.etapa-1, len(proj.tempo)):
            resTime = proj.tempo[e] #número de períodos que faltam para conlcuir a etapa
            i=0
            while i < resTime:
                if init:
                    eCusto = eCusto + (1/((1+self.txDesc)**(eTime)))*proj.modos[e][modoinit].nrn*(1/(1-proj.modos[e][modoinit].probAtr)) #trazendo para o presente 
                    eTime = eTime + (1/(1-proj.modos[e][modoinit].probAtr)) # tempo esperado para concluir o período considerando o atraso  
                    init = 0
                    i = i + proj.modos[e][modoinit].deltat
                else:
                    eCusto = eCusto + (1/((1+self.txDesc)**(eTime)))*proj.modos[e][0].nrn*(1/(1-proj.modos[e][0].probAtr)) #trazendo para o presente 
                    eTime = eTime + (1/(1-proj.modos[e][0].probAtr)) # tempo esperado para concluir o período considerando o atraso  
                    i = i + proj.modos[e][0].deltat
        eTime = eTime + proj.tCheg # deve-se partir do tempo atual
        return [eTime, eCusto] 

    def SelectMaxModo(self, proj):
        vplMax = 0
        modoMax = 0
        pEtapa = proj.etapa -1
        for mod in range(len(proj.modos[pEtapa])):
            ePerf = self.CalcPerfEsp(proj, mod)
            [eTime,eCusto] = self.CalcTimeEsp(proj, mod) 
            vp = proj.valorLanPerf(eTime, ePerf)/((1+self.txDesc)**(eTime -proj.tCheg))
            if (mod==0):
                vplMax = vp - eCusto
            else:
                if(vplMax <= vp - eCusto):
                    modoMax = mod
                    vplMax = vp - eCusto
            
        return (vplMax,modoMax)

# Classe Simulador
class Simulador:
	def simulacao(self, S, Pol, niter, vmax):
		vlist = []
		vlist2 = []
		vlist3 = []
		vlist4 = [] 
		v0 = 0
		bf.save_cabecalho(S,'teste_saida.txt')
		for n in range(niter):
			print('iteracao ' + str(n) + ': \n')		
			S.imprime()
			print('\n\n')
			d = Pol.solver(S)
			custoSim = d.valor
			vlist3.append(custoSim)
			valorSim = S.transicao(d,vmax)
			vlist4.append(valorSim)
#            print ('Valor Simulado:' + str(valorSim))
#            print ('custo Simulado:' + str(custoSim))
			vlist.append(valorSim - custoSim)
			v0 = 0.995*v0 + 0.005*(valorSim - custoSim)
			vlist2.append(v0)
			bf.save_data(S,[valorSim - custoSim,v0,custoSim,valorSim],'teste_saida.txt')
		S.imprime()
		return [vlist,vlist2,vlist3,vlist4]

class ADP(tpd.Trainer):
##@b approxPIA
#@brief Algoritmo da Figura 10.10 de Power(2011), Dado uma política inicial, encontra uma política "ótima" a partir de uma estratégia de #aprendizado
#@details
# --
# 
# 
#@param P objeto instanciado da classe Problema que possua, funções de custo, função de transição e estado
#@param A política inicial:  objeto instanciado da classe Politica que dado um estado retorna uma ação
#@param n número de iterações do Policy Iteration Algorithm
#@param m tamanho da simulção de Monte Carlo para convergência do valor
#@retval Alinha: objeto instanciado atualizado da classe Politica que dado um estado retorna uma ação
	def approxPIA(P,A,n,m):
		lpar = [P.y1,P.y2,P.te, P.ts]
		Stat = []
		Alinha = c.deepcopy(A) #step 4: inicializar a política
		for i in range(n):
			Sm = Estado(P.P_ini,P.lst_silos) #iniciar o estado inicial (step 2)
			Am = c.deepcopy(Alinha)
			for j in range(m):
				Smp1 = c.deepcopy(Sm) 
				#step 5: gera a incerteza do cenário 
				a = Alinha.solver(Smp1,lpar) #gerar a ação com a política atual step 6a
				custo = Alinha.retorno(Smp1,lpar)
				Smp1.transicao(a) # gerar novo estado a partir da transição do atual
				Am.updPol(Am,a,Sm,Smp1,lpar)
				Stat.append([custo] + Am.getStatistics())
				del(Sm)
				Sm = c.deepcopy(Smp1)
				del(Smp1)
			del(Alinha)
			Alinha = c.deepcopy(Am) #step 8: atualizar a política para a iteração i+1
			del(Am)
		self.adpStat(['custo'] +Alinha.getStatLabels(),Stat,n,m)
		return Alinha

	def adpStat(labels,Stats,n, m):
		self.StatLab = labels
		self.StatData = [[] for i in range(len(labels))]
		for i in range(len(labels)):
			for j in range(n):
				auxn = []
				for k in range(m):
					auxn.append(Stat[j*n+k][i])
			self.StatData[i].append(auxn)
	 

	def graficoStat(self,idStat):
		n = len(self.StatSata)
		m = len(self.StatData[0])		    
		s= range(n*m)
		matplotlib.pyplot.figure(figsize=(30,30))
		matplotlib.pyplot.scatter(s,self.Statdata[idStat],label= self.StatLab)

		matplotlib.pyplot.xlabel("Iteração")
		matplotlib.pyplot.ylabel("Valor")
		matplotlib.pyplot.show()
	 


# Instancia gerada manualmente

vprob = 0.5
vprobat = 0.3
vdelta = 0.5
vdeltat = 1
lnrn = 30
vnome = "Continuar"
M1 = Modo(vprob, vprobat, vdelta, lnrn, vdeltat, vnome)

vprob = 0.75
vprobat = 0.3
vdelta = 1
vdeltat = 1
lnrn = 40
vnome = "Melhorar"
M2 = Modo(vprob,vprobat, vdelta, lnrn, vdeltat, vnome)

lmodo = [[M1,M2],[M1,M2]]

lpar =[65, 30, 21, 4, 0, 0.3]
vdiv = 0
ltempo = [2,3]
vcmax = 0
varea = "A1"
vnome = "p1"

p1 = Projeto(lmodo, lpar, vdiv, ltempo, vcmax, varea,1, vnome,0)        

vprob = 0.1
vprobat = 0.2
vdelta = 0.5
vdeltat = 1
lnrn = 10 
vnome = "Continuar"
M1 = Modo(vprob,vprobat, vdelta, lnrn, vdeltat, vnome)

vprob = 0.4
vprobat = 0.1
vdelta = 0.8
vdeltat = 1
lnrn = 12 
vnome = "Melhorar"
M2 = Modo(vprob,vprobat, vdelta,lnrn, vdeltat, vnome)

lmodo = [[M1,M2],[M1,M2]]

lpar =[30, 20, 21, 4, 0, 0.6]
vdiv = 1
ltempo = [0,1]
vcmax = 1
varea = "A1"
vnome = "p2"

p2 = Projeto(lmodo, lpar, vdiv, ltempo, vcmax, varea,2, vnome,0)


vprob = 0.8
vprobat = 0.3
vdelta = 0.3
vdeltat = 1
lnrn = 11 
vnome = "Continuar"
M1 = Modo(vprob,vprobat, vdelta, lnrn, vdeltat, vnome)

vprob = 0.35
vprobat = 0.2
vdelta = 0.7
vdeltat = 1
 
lnrn = 15
vnome = "Melhorar"
M2 = Modo(vprob,vprobat, vdelta,  lnrn, vdeltat, vnome)

lmodo = [[M1,M2],[M1,M2]]

lpar =[32, 18, 21, 4, 0, 0.4]
vdiv = 0
ltempo = [1,2]
vcmax = 0
varea = "A2"
vnome = "p3"

p3 = Projeto(lmodo, lpar, vdiv, ltempo, vcmax, varea,1, vnome,0)

vprob = 0.5
vprobat = 0.8
vdelta = 0.1
vdeltat = 1

lnrn = 14
vnome = "Continuar"
M1 = Modo(vprob,vprobat, vdelta,  lnrn, vdeltat, vnome)

vprob = 0.5
vprobat = 0.8
vdelta = 0.3
vdeltat = 1

lnrn = 18
vnome = "Melhorar"
M2 = Modo(vprob,vprobat, vdelta, lnrn, vdeltat, vnome)

vprob = 0.5
vprobat = 0.1
vdelta = 0.7
vdeltat = 1

lnrn = 20
vnome = "Acelerar"
M3 = Modo(vprob,vprobat, vdelta, lnrn, vdeltat, vnome)

lmodo = [[M1,M2,M3],[M1,M2,M3]]

lpar =[27, 20, 21, 4, 0, 0.1]
vdiv = 0
ltempo = [2,3]
vcmax = 0
varea = "A2"
vnome = "p4"

p4 = Projeto(lmodo, lpar, vdiv, ltempo, vcmax, varea,1, vnome,0)

vprob = 0.4
vprobat= 0.4
vdelta = 0.2
vdeltat = 1
 
lnrn = 24
vnome = "Continuar"
M1 = Modo(vprob,vprobat, vdelta, lnrn, vdeltat, vnome)

vprob = 0.5
vprobat = 0.1
vdelta = 0.9
vdeltat = 1

lnrn = 36
vnome = "Melhorar"
M2 = Modo(vprob,vprobat, vdelta, lnrn, vdeltat, vnome)

lmodo = [[M1,M2],[M1,M2]]

lpar =[36, 24, 21, 4, 0, 0.8]
vdiv = 0
ltempo = [0,1]
vcmax = 0
varea = "A2"
vnome = "p5"

p5 = Projeto(lmodo, lpar, vdiv, ltempo, vcmax, varea,2, vnome,0)
        
P  = [p1, p2,p3, p4, p5]

vfi = 0.5
vbe = 0.1
vroum = 0.1
vrodois = 0.1
lqrn = 70
lareas = ["A1", "A2", "A3"]
letapas = [1, 2]

S = Estado_GCPDNP(P, vfi, vbe, vroum, vrodois, lqrn, lareas, letapas)

S.imprime()
Pol = Politica() 
'''d = Pol.solver(S)
d.imprime()
S.transicao(d,2)
S.imprime()'''

sim = Simulador()
[rl1,rl2,rl3,rl4] = sim.simulacao(S,Pol,2000,2)

#print rl1
#print rl2

#GraficoLinha(rl1[0:1999])
#GraficoLinha(rl2[0:1999])

# Instancia gerada atraves do Gerador
'''
G = Gerador(3,3)
lareas = G.geraAreas()
letapas= G.geraEtapas()
lqrn = G.geraRecNRen()
p1 = G.geraProjeto(1,letapas,lareas,lqrn)
p2 = G.geraProjeto(2,letapas,lareas,lqrn)
p3 = G.geraProjeto(3,letapas,lareas,lqrn)
p4 = G.geraProjeto(4,letapas,lareas,lqrn)
p5 = G.geraProjeto(5,letapas,lareas,lqrn)
p6 = G.geraProjeto(6,letapas,lareas,lqrn)

P  = [p1, p2,p3, p4, p5, p6]
vfi = 0.5
vbe = 0.1
S = Estado_GCPDNP(P, vfi, vbe, lqrn, lareas, letapas)

# Impressao dos resultados
S.imprime()
Pol = Politica() 
Pol.solver(S)
'''
