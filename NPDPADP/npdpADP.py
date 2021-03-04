#coding: utf-8
import sys
sys.path.append('../')
from Leitor.leitorXML import *
from gurobipy import *
import math
# from cStringIO import StringIO
import numpy as np
from scipy.stats import norm
import NPDPADP.basisfunction as bf
import numpy.linalg as npla
from numpy import array, zeros, sqrt, shape, eye
import copy as c
import Gerador.gerador as G
import matplotlib.pyplot
import pandas as pd
#import xlwt
#import xlrd
#import datetime
#import operator

#import matplotlib.pyplot as plt



#stepsize rules

def stpsze_ln50up100(it):
	ss = 0.5 + min(it/200,0.5)
	return ss

def stpsze_ln100dn80(it):
	ss = 1 - min(it/500,0.2)
	return ss
def stpsze_cte1(it):
	return 1

def switch_stpsze(argument):
	switcher = {
		'ln50up100': stpsze_ln50up100,
		'ln100dn80': stpsze_ln100dn80,
		'cte1': stpsze_cte1
	}
	return switcher.get(argument, lambda *args: "Invalid Lambda")


# Modelo


# Definicao das Classes

# Classe Problema


class Problema:
	# Classe com os parametros que definem a instancia do problema
	def __init__(self, *args, **kwargs):
		#(self, vqCheg,lProj, vfi, vbe, vroum, vrodois, lqrn, lareas, letapas,c):
		if len(args) ==1:
			geraDict = LerXML(args[0])
			self.instFile = str(geraDict['@ArqName'])
			self.caminho = str(geraDict['Caminho'])

			prob = geraDict['Problema']
			self.lareas = range(int(prob['nA']))
			self.letapas = [i+1 for i in range(int(prob['nE']))]
			self.tx = 0.01
			self.vqCheg = int(prob['maxCheg'])
			self.vfi = float(prob['vfi'])
			self.vbe = float(prob['vbe'])
			self.vro1 = float(prob['ro1'])
			self.vro2 = float(prob['ro2'])
			self.lqrn = float(prob['qRec'])
			
			projetos = prob['Projeto']
			self.P = []
			for p in projetos:
				self.P.append(self.lerProj(p))


		else:
			if (len(args) == 10):
				self.qCheg = vqCheg # Quantidade maxima de chegadas por periodo
				self.P = lProj
				self.vfi = vfi
				self.vbe = vbe
				self.vro1 = vroum
				self.vro2 = vrodois
				self.lqrn = lqrn
				self.lareas = lareas
				self.letapas = letapas
				self.caminho = c

			else:
				print('Gerador(): Erro na passagem de parametros')
				sys.exit(1)



		self.S = Estado_GCPDNP(self.P, self.vfi, self.vbe, self.vro1, self.vro2, self.lqrn, self.lareas, self.letapas,self.tx)
		self.Simul = Simulador()

	def definePol(self,A):
		self.Pol = A
	def lerProj(self,dicP):

		vnome = dicP['nome']
		Modos = dicP['Modos']
		Mx = float(dicP['Mx'])
		mn = float(dicP['mn'])
		a = float(dicP['a'])
		pk = float(dicP['pk'])
		mu = float(dicP['mu'])
		desvp = float(dicP['pk'])
		lpar = [Mx,mn,a,pk,mu,desvp]

		vdiv = int(dicP['div'])
		tCheg = int(dicP['tCheg'])
		varea = int(dicP['area'])
		vetapa = int(dicP['etapa'])
		cmax = int(dicP['cmax'])

		tempo = dicP['tempo']
		ltempo = []
		for t in tempo:
			ltempo.append(float(t))

		print(Modos)
		lmodo = []
		for m in Modos:
			print('\n\tmodo0: {} '.format(m['Modo']))
			lmodo.append(self.lerModo(m['Modo']))

		p3 = Projeto(lmodo, lpar, vdiv, ltempo, cmax, varea,vetapa, vnome,tCheg)
		return p3
		 
	def lerModo(self,dicM):
		print('\n\tdicM: {}'.format(dicM))
		mE = []	
		for m in dicM:
			print('\n\tmodo1: {}'.format(m))
			vnome = m['nome']
			vprob = float(m['prob'])
			vprobat =  float(m['probAtr'])
			vdelta =  float(m['deltap'])				   
			lnrn =  float(m['nrn'])
			vdeltat=  float(m['deltat'])
			mE.append(Modo(vprob,vprobat, vdelta, lnrn, vdeltat, vnome))
		return mE
  
'''

		<xs:element name="nome" type="xs:string"/>
		<xs:element name="prob" type="xs:float"/>
		<xs:element name="probAtr" type="xs:float"/>
		<xs:element name="deltap" type="xs:float"/>
		<xs:element name="nrn" type="xs:float"/>
		<xs:element name="deltat" type="xs:float"/>
'''


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

	def getMinCostToGo(self,idetapa,deltat = 0):
		idetp = idetapa
		tRes = self.tempo[idetp] - deltat
		if tRes <=0:
			idetp = idetp +1
			tRes = 0

		cmin = 0
		for e in range(idetp, len(self.modos)):
			if e > idetp:
				tRes = self.tempo[e]  # assume que não haverá atraso
			cmodmin=0
			for m in range(len(self.modos[e])):
				if(m==0):
					cmodmin = self.modos[e][0].nrn
				else:
					if(cmodmin>self.modos[e][m].nrn):
						cmodmin = self.modos[e][m].nrn

			cmin = cmin + cmodmin*tRes
		return cmin

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
	def CalcTimeEsp(self):
		eTime = 0
		for e in range(self.etapa-1, len(self.tempo)):
			resTime = self.tempo[e] #número de períodos que faltam para conlcuir a etapa
			eTime = eTime + (1/(1-self.modos[e][0].probAtr))*resTime # tempo esperado para concluir o período considerando o atraso
		return eTime
	def valorLan(self,t,dp=0):
		v1 =  (self.par[0] - self.par[1])*np.exp(-((t-self.tCheg)/self.par[2])**self.par[3])*(1 - norm.pdf(self.performance+dp, self.par[4],self.par[5])) + self.par[1]
		#print ('VALOR LAN :'+str(v1))
		return v1
	def vplLan_esp(self,tlan,tx,dp=0):
		#tlan neste caso significa em quantos períodos a partir do estágio atual o projeto será lançado
		v1 = self.valorLan(tlan,dp)*np.exp(-tlan*tx)		#print ('VALOR LAN :'+str(v1))
		return v1
	def valorLan_mn(self,tlan,tx):
		#t neste caso significa em quantos períodos a partir do estágio atual o projeto será lançado
		v1 =  self.par[1]*np.exp(-tlan*tx)
		#print ('VALOR LAN :'+str(v1))
		return v1
	def valorLan_mx(self,tlan,tx):
		#t neste caso significa em quantos períodos a partir do estágio atual o projeto será lançado
		v1 =  self.par[0]*np.exp(-tlan*tx)
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
				print(mod.nome)
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
	def __init__(self, lprojeto, vfi, vbe,vroum,vrodois, vqrn, lareas, letapas,tx):
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
		self.Vt = 0
		self.tx = tx
		
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
			print(p.nome)
			print('lista de tempos: '+ str(p.tempo) + '\n')
			print('Etapa: '+ str(p.etapa) + '\n')			
		print('Pc: \n ')
		for p in self.Pc:
			print(p.nome)
		print('Pl: \n ')
		for p in self.Pl:
			print(p.nome)
		print('P_a: \n ')
		for a in range(len(self.A)):
			print('Area '+ str(a) + ':\n')		 
			for p in self.P_a[a]:
				print(p.nome)
		print('P_e: \n ')
		for e in range(len(self.E)):
			print('Etapa '+ str(e) + ':\n')		 
			for p in self.P_e[e]:
				print(p.nome)
	def Calc(self):
		# VALOR REAL DA FUNCAO OBJETIVO
		# RETORNO DOS PROJETOS QUE FORAM LANÇADOS
		# CUSTO DOS PROJETOS QUE ESTÃO SENDO EXECUTADOS
		return self.Vt
	# Recebe decisao

	def transicao(self,dec,vqMax):
		print('#################################### TRANSICAO')
		for pi in self.P:
			print(f'{pi.nome}:{pi.etapa}')
		dec.imprime()
		Incerteza = GeraIncerteza(self,dec,self.estagio,vqMax)
		Incerteza.geracao()
		for pi in self.P:
			print(f'{pi.nome}:{pi.etapa}')
		self.Vt = Incerteza.CalcValor() - dec.valor # dec.valor é um custo registrado como positivo
		# Passagem de estagio
		self.estagio = self.estagio + 1
		newPe = Incerteza.Pe
		print('NOVOS: ')
		for np in Incerteza.newP:
			print(f'{np.nome}: {np.etapa}, {np.tempo}')

		# Adicionando os novos projetos na primeira etapa
		newPe[0] = newPe[0] + Incerteza.newP 
		self.P = []
		for e in range(len(self.E)):
			self.P_e[e] = newPe[e]
			self.P = self.P + newPe[e]
		self.P_a = [[p for p in self.P if p.area == a] for a in self.A]
		self.Pc = [p for p in self.P if (p.div) & (p.congatual < p.cmax)]
		self.Pl = [p for p in self.P if (p.etapa == self.E[len(self.E)-1]) & (p.tempo[self.E.index(p.etapa)] == 1)]
		self.imprime()
		return self.Vt #custo do estado t calculado durante a transição para t+1

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
		self.valor = vvalor #custo!!
		# Os valores sao colocados de forma a decidir qual projeto continua, e cancelado ou congelado
		self.Abandonados = [p for p in range(len(self.y)) if self.y[p] == 1]
		self.Congelados = [p for p in range(len(self.f)) if self.f[p] == 1]
		self.Executados = [p for p in range(len(self.w)) if sum(self.w[p]) == 1]
		self.ExecModo =  [self.w[p].index(1) for p in self.Executados]

	def imprime(self):
		print('id Abandonados: ' + str(self.Abandonados)+ '\n')
		print('id Congelados: '+ str(self.Congelados) + '\n')
		print('id Executados: '+ str(self.Executados) + '\n')
		print('id Modos: '+ str(self.ExecModo) + '\n')
		
  
	
# Classe GeraIncerteza		 
class GeraIncerteza:
	def __init__(self, vEstado, vDecisao,vnEstagio,vqMax):
		# X: recebe o valor do estado
		self.X = vEstado
		# U: recebe a decisao corrente
		self.U = vDecisao
		self.Gen = G.Gerador(0,0,0,0)
		self.qnk = vEstado.qn_k
		self.Pe = []
		self.newP = []
		self.t = vnEstagio
		self.qMax = vqMax
		self.ValorAT = 0 
# Calcula retorno gerado pelo lançamento após a realizacao da incerteza
	def CalcValor(self):
		ret = 0
		#print('self.Pe[len(self.Pe)-1]' +str(self.Pe[len(self.Pe)-1]))
		for p in self.X.Pl:
			#print ('p.tempo: ' + str(p.tempo[len(self.Pe)-1]))
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
				print('Etapa {} -  nome: {}, pid: {}'.format(e,p.nome,pid))
				#print('Exec: {}'.format(self.U.Executados))
				#print('Aband: {}'.format(self.U.Abandonados))
				#print('Congelados: {}'.format(self.U.Congelados))

				if (pid not in self.U.Abandonados):
					if (pid in self.U.Executados):
						modid = self.U.Executados.index(pid)
						mod = self.U.ExecModo[modid]
						print(f'projeto {p.nome} Executado com o modo {mod}')
						[newPe, bAtr] = self.geraIncertezaHuz5(p, mod)
						if (not bAtr):
							newPe = self.geraIncertezaHuz3(newPe, mod)
						else:
							print('projeto' + str(newPe.nome) + ' ATRASOU')
					else:
						if (p in self.X.Pc):
							pidc = self.X.Pc.index(p)
							if (pidc in self.U.Congelados):
								print(f'projeto {p.nome} congelado')
								newPe = p
								[newPe,bAtr] = self.geraIncertezaHuz5(newPe,-1)
							else:
								print('projeto ' + str(p.nome) + ' NÃO ALOCADO')
						else:
							print('projeto ' + str(p.nome) + ' NÃO ALOCADO not in pc')

					newPe = self.geraIncertezaHuz1(newPe)
					newPe = self.geraIncertezaHuz4(newPe)
					print(f'tempo:{newPe.tempo},etapa{newPe.etapa}')
					for modi in newPe.modos[newPe.etapa-1]:
						idm = newPe.modos[newPe.etapa-1].index(modi)
						if(modi.deltat>newPe.tempo[newPe.etapa-1]): 
							del(newPe.modos[newPe.etapa-1][idm])
					if(newPe.tempo[newPe.etapa-1]>0): #ainda nao terminou nesta etapa
						nPe.append(newPe)
					else: # terminou, adicionar no proximo conjunto
						newPe.etapa = newPe.etapa + 1
						nextPe.append(newPe)
				else:
					if pid in self.U.Abandonados:
						print('projeto' + str(p.nome) + ' ABANDONADO')
					else:
						print('projeto' + str(p.nome) + ' NÃO ALOCADO')
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

	def __init__(self,lbs,lcoef, gam,c):
		self.lBasis = lbs 
		self.B = eye(len(lcoef))
		self.Theta = array(lcoef)
		self.gamma = gam
		self.caminho = c
		self.log = 0

	def setLog(self, b):
		self.log = b
	def resetB(self):
		#self.B = eye(len(self.lBasis))
		return 0

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
		for p in estado_x.Pc:
			f.append(m.addVar(vtype = GRB.BINARY, name = "f[{}]". format(p.nome)))
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

	# Criar uma variável para cada basi function
		vbasis = []
		for b in range(len(self.lBasis)):
			vbasis.append(m.addVar(vtype=GRB.CONTINUOUS, name="vbasis[{}]".format(b)))


# Função Objetivo
		# a realização da incerteza vai gerar o retorno dos projetos lançados em t+1, em t não é definido pelas decisões
		exp = - quicksum(tn[e] for e in range(len(estado_x.E)))
		exp = exp - quicksum(V[a]*estado_x.roum for a in range(len(estado_x.A))) # O que é isso?
		exp = exp - quicksum(J[e][idp]*estado_x.rodois for e in range(len(estado_x.E)) for idp in range(len(estado_x.P_e[e]))) # O que é isso?
		exp = exp + quicksum(self.Theta[i]*vbasis[i] for i in range(len(self.lBasis))) # Parcela referente às Basis Functions
		m.setObjective(exp, GRB.MAXIMIZE)

# Restrições

	#Restrição 0: Basis Functions
		for b in range(len(self.lBasis)):
			m.addConstr(vbasis[b] - self.lBasis[b].Restr(estado_x, [w,f,y,tn,V,J,mn,Quota,cmin]) == 0)

	# Restrição 1: Status dos projetos que não podem ser congelados 
		PmPc = [p for p in estado_x.P if p not in estado_x.Pc]
		for p in PmPc:
			ip = estado_x.P.index(p)
			m.addConstr(y[ip] + quicksum(w[ip][mod] for mod in range(len(p.modos[estado_x.E.index(p.etapa)]))) == 1)
		
	# Restrição 2: Status dos projetos que podem ser congelados 
		for p in estado_x.Pc:
			ip = estado_x.P.index(p)
			ipc = estado_x.Pc.index(p)
			m.addConstr(y[ip] + f[ipc] +quicksum(w[ip][mod] for mod in range(len(p.modos[estado_x.E.index(p.etapa)]))) == 1)
		
	# Restrição 3: O somatório das necessidades de recursos dos projetos ativos deve ser igual a quantidade disponível por etapa
		for e in range(len(estado_x.E)):
			m.addConstr( quicksum(quicksum(w[estado_x.P.index(estado_x.P_e[e][idp])][mod]*estado_x.P_e[e][idp].modos[e][mod].nrn for mod in range(len(estado_x.P_e[e][idp].modos[e]))) for idp in range(len(estado_x.P_e[e])) ) == tn[e] )
	 
	# Restrição 4: Um projeto nao poderá capturar todo o recurso disponível por etapa
		for e in range(len(estado_x.E)):
			for p in range(len(estado_x.P_e[e])):
				m.addConstr(quicksum(w[estado_x.P.index(estado_x.P_e[e][p])][mod]*estado_x.P_e[e][p].modos[e][mod].nrn for mod in range(len(estado_x.P_e[e][p].modos[e]))) <=  estado_x.fi*tn[e]+ J[e][p]*estado_x.qn_k)

	# Restrição 5a: Uma área nao poderá capturar todo o recurso disponível
		for a in range(len(estado_x.A)):
			#print('a s: '+ str(a) + '\n')
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
			vy.append(int(round(y[p].x,2)))
		
		vf = []
		for p in range(len(estado_x.Pc)):
			vf.append(int(round(f[p].x)))

		vw = []
		for p in range(len(estado_x.P)):
			vlinha = []
			ie = estado_x.E.index(estado_x.P[p].etapa)
			for mod in range(len(estado_x.P[p].modos[ie])):	
				vlinha.append(int(round(w[p][mod].x)))
			vw.append(vlinha)
		#print(str(vw) + 'VW')
		vtn = []
		for e in range(len(estado_x.E)):
			vtn.append(tn[e].x)

		print('SOLUCAO:\n')
		for p in range(len(estado_x.P)):
			if (int(round(y[p].x))>0):
				print(estado_x.P[p].nome +' foi cancelado'+ f' y = {y[p].x}')
			else:
				for mod in range(len(w[p])):
					if(int(round(w[p][mod].x))>0):
						print(estado_x.P[p].nome +' foi executado com o modo '+ estado_x.P[p].modos[estado_x.E.index(estado_x.P[p].etapa)][mod].nome + f' w = {w[p][mod].x}')
		for p in range(len(estado_x.Pc)):
			if (int(round(f[p].x))>0):
				print(estado_x.Pc[p].nome +' foi congelado' + f' f = {f[p].x}')

		print('RESPOSTA - PL:')
		print('faturamento: ')
		for p in estado_x.Pl:
			print(p.nome)
			print('etapa: ' + str(p.etapa))
			for mod in range(len(p.modos[estado_x.E.index(p.etapa)])):
				if(w[estado_x.P.index(p)][mod].x>0.0001):
					print('mod :' + str(mod))
					print('w :' + str(w[estado_x.P.index(p)][mod].x))
					print('valor :' + str(p.valor(mod,estado_x.estagio)))
					print ('\n')
		print('Custos: ')
		for p in estado_x.P:
			print(p.nome)
			print('etapa: ' + str(p.etapa))
			for mod in range(len(p.modos[estado_x.E.index(p.etapa)])):
				if(w[estado_x.P.index(p)][mod].x>0.0001):
					print('mod :' + str(mod))
					print('w :' + str(w[estado_x.P.index(p)][mod].x))
					print('custo :' + str(p.modos[p.etapa -1][mod].nrn))
					print ('\n')

				
		Valor = sum([tn[e].x for e in range(len(estado_x.E))])
		Valor = Valor + sum([V[a].x*estado_x.roum for a in range(len(estado_x.A))])
		Valor = Valor + sum([sum([J[e][idp].x*estado_x.rodois for idp in range(len(estado_x.P_e[e]))]) for e in range(len(estado_x.E))])
	
		d = Decisao(vy, vf, vw, vtn, obj,Valor)
		return d
	def retorno(self,EstX,lpar,decisao):
		return 0
	def calc_erro_m(self,C,fgf):
		#print('Função Calc_erro_m\n \tC: {} \n\t fgf: {} \n\t Theta:{}'.format(C,fgf,self.Theta))
		aux = npla.multi_dot([fgf,self.Theta]) #calcula o produto escalar de fgf e teta
		return C - aux #retorna o erro

	def calc_denm(self,phi,fgf): #calcula o denominador de teta
		#print("COMPARANDO DENOMNADORES:")
		m1 = np.matmul(self.B, np.transpose(np.matrix(phi)))
		m2 = np.matmul(np.matrix(fgf),m1)
		#print (m2[0,0])
		#a2 = np.transpose(fgf)
		#a3 =  np.matmul(np.matmul(fgf,self.B),phi)
		#print(a3)
		
		denm = 1.0 + m2[0,0] # denominador
		if (denm>0.0)&(denm<0.00001):
			denm +=0.0001 #to avoid numerical issues; 
		else: 
			if (denm<0.0)&(denm >-0.00001): 
				denm -=0.0001; #to avoid numerical issues
		return denm

	def UpdateB_m(self,phi_m, fgf):
		texto = []
		texto.append("\n\n###############################################\n")
		texto.append('\tIT: {}\n'.format(self.it))
		texto.append('\tB: {}\n'.format(self.B))
		#print('\tshape B: {}\n'.format(self.B.shape))
		#print('\tshape phi_m: {}\n'.format(np.matrix(phi_m).shape))
		#print('\tshape fgf: {}\n'.format(np.matrix(fgf).shape))

		texto.append('\tshape B: {}\n'.format(self.B.shape))
		texto.append('\tshape phi_m: {}\n'.format(np.matrix(phi_m).shape))
		texto.append('\tshape fgf: {}\n'.format(np.matrix(fgf).shape))
		denm = self.calc_denm(phi_m,fgf) #calcula o denominador da formula de B
		texto.append('\tdenm: {}\n'.format(denm))
		mult1 = np.matmul(np.transpose(np.matrix(phi_m)),np.matrix(fgf))
		texto.append('\tmult1: {}\n'.format(mult1))
		mult2 = np.matmul(self.B,mult1)
		texto.append('\tmult2: {}\n'.format(mult2))
		mult = np.matmul(mult2,self.B)
		#print('\tmult: {}, shape {}\n'.format(mult, mult.shape))
		texto.append('\tmult: {}, shape {}\n'.format(mult, mult.shape))
		self.B = self.B - float((1/denm))*mult #atualiza B pela formula
		texto.append('\tapos atualizar B: {}\n'.format(self.B))
		if self.log:
			arquivo = self.caminho + 'Log/' + 'saida_B.txt'
			arq = open(arquivo, 'a')
			arq.writelines(texto)
			arq.close()
		del (texto)


	def UpdateTheta_m(self,erro,phi,fgf):
		texto = []
		texto.append("\n\n###############################################\n")
		texto.append('\tIT: {}\n'.format(self.it))
		texto.append('\tTheta: {}\n'.format(np.matrix(self.Theta)))
		#print('\tshape Theta: {}\n'.format(self.Theta.shape))
		#print('\tshape phi: {}\n'.format(np.matrix(phi).shape))
		#print('\tshape fgf: {}\n'.format(np.matrix(fgf).shape))

		texto.append('\tshape Theta: {}\n'.format(np.matrix(self.Theta).shape))
		texto.append('\tshape phi: {}\n'.format(np.matrix(phi).shape))
		texto.append('\tshape fgf: {}\n'.format(np.matrix(fgf).shape))
		
		denm = self.calc_denm(phi,fgf) #calcula o denominador da formula de teta
		texto.append('\tdenm: {}\n'.format(denm))
		m1 = erro*np.matmul(self.B,np.transpose(np.matrix(phi)))
		texto.append('\tm1: {}\n'.format(m1))
		m2 = (1/denm)*m1
		texto.append('\tm2: {}\n'.format(m2))
		newTh = np.matrix(self.Theta) + np.transpose(m2)
		self.Theta = array(newTh)[0]  #atualiza theta pela formula
		texto.append('\tapos atualizar Theta: {}\n'.format(self.Theta))
		if self.log:
			arquivo = self.caminho + 'Log/' + 'saida_Theta.txt'
			arq = open(arquivo, 'a')
			arq.writelines(texto)
			arq.close()
		del(texto)
		
#@param S Estado
#@param lpar lista de parâmetros do problema = [y1, y2, te, ts]
	def calc_phi(self, S, lpar):
		#basis* indicadores
		phi  = [self.lBasis[i].Calc_phi(S) for i in range(len(self.Theta))]#chama as políticas
		a_phi = array(phi)
		#print (a_phi)
		#print("-----")
		return a_phi #retorna os resultados das políticas 

#@param S Estado
#@param Smp Estado após a transição
#@param lpar lista de parâmetros do problema = [y1, y2, te, ts]
	def calc_phiGammaPhi(self, S,Smp,lpar):
		phi_m = self.calc_phi( S,lpar) #calculo de phi usando o estado antes da transição
		phi_mp = self.calc_phi( Smp,lpar) #calculo de phi usando o estado depois da transição
		phiGammaPhi = phi_m - self.gamma*phi_mp # operação matricial
		return phiGammaPhi #phiGammaPhi

#@param	self Política 
#@param	a retorno da classe solver [d=x,fit,custo]
#@param Sm Estado
#@param Smp1 Estado após a transição
#@param lpar lista de parâmetros do problema = [y1, y2, te, ts]
	def updPol(self,a,Sm,Smp1,lpar):
		texto = []
		texto.append("\n\n###############################################\n")
		texto.append('\tIT: {}\n'.format(self.it))
		texto.append('\tTheta: {}\n'.format(self.Theta))
		texto.append('\tB: {}\n'.format(self.B))
		#recursive least squares
		#step 6d algoritmo 10.10 pag 407
		#custo = self.retorno(Sm,lpar,a.x) #para calcular o custo a.x:movimento a ser realizado
		custo = Smp1.Calc() #retorna o valor do estado anterior calculado durante a transição
		texto.append('\tC^m: {}\n'.format(custo))
		#print("CONFERINDO CUSTO")
		#print(custo)
		#print(custo[1])
		#print(a.fit)
		phi_m = self.calc_phi(Sm,lpar) #chama a função calc_phi, phi_m = resultados das políticas
		texto.append('\tphi_m: {}\n'.format(phi_m))
		fgf =  self.calc_phiGammaPhi(Sm,Smp1,lpar) #chama a função calc_phiGammaPhi, #phiGammaPhi é a diferença dos valores da política antes e depois da transição ??? = fgf = passo 6d
		texto.append('\tfgf: {}\n'.format(fgf))

		#setp 7b alg 10.10 pag 407 - eq. 10.23 via rls - tem que calcular erro, b e teta
		erro = self.calc_erro_m(custo,fgf) #calcula o erro
		texto.append('\terro: {}\n'.format(erro))
		self.UpdateTheta_m(erro,phi_m, fgf) #atualiza teta
		texto.append('\tapos atualizar Theta: {}\n'.format(self.Theta))
		self.UpdateB_m(phi_m, fgf) #atualiza B
		texto.append('\tapos atualizar B: {}\n'.format(self.B))
		if self.log:
			arquivo = self.caminho + 'Log/' + 'saida_updpol.txt'
			arq = open(arquivo, 'a')
			arq.writelines(texto)
			arq.close()
		del(texto)
		return erro

	def getStatLabels(self):
		thetafb =['Theta_fb'+ str(i) for i in range(len(self.lBasis))]
		return thetafb

	def getStatistics(self):
		return self.Theta





'''
class Politica_GulosaVPL:
	def __init__(self, ParPol):
		self.txDesc = ParPol[0]
	
	def solver(self,EstX):
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
'''
# Classe Simulador
class Simulador:
	def simulacao(self, S, Pol, niter, vmax,caminho):
		vlist = []
		vlist2 = []
		vlist3 = []
		bf.save_cabecalho(S,caminho+'Log/teste_saida.txt')
		for n in range(niter):
			print('iteracao ' + str(n) + ': \n')		
			S.imprime()
			print('\n\n')
			d = Pol.solver(S)
			custoSim = d.valor
			vlist3.append(custoSim)
			valorSim = S.transicao(d,vmax)
			vlist2.append(valorSim+custoSim)
#			print ('Valor Simulado:' + str(valorSim))
#			print ('custo Simulado:' + str(custoSim))
			vlist.append(valorSim)
			bf.save_data(S,[valorSim,valorSim + custoSim,custoSim],caminho+'Log/teste_saida.txt')
		S.imprime()
		return [vlist,vlist2,vlist3]


#class ADP(tpd.Trainer):
class ADP:
	def __init__(self, c):
		self.caminho = c
		self.log = 0
		self.PStat = 0

	def setPrintStat(self, b):
		self.PStat = b
	def setLog(self, b):
		self.log = b
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
	def approxPIA(self,Prob,A,n,m):
		texto=[]
		lpar = [Prob.vqCheg,Prob.vfi,Prob.vbe,Prob.vro1, Prob.vro2,Prob.lqrn,Prob.lareas,Prob.letapas]
		Stat = []
		Stat_basis = []
		Alinha = c.deepcopy(A) #step 4: inicializar a política
		Sm = c.deepcopy(Prob.S)
		for i in range(n):
			texto.append("\n\n#######################################################################\n")
			texto.append("\tFuncao approxPIA(self,P,A,n,m) iteracao {}\n".format(i))
			texto.append("\tTheta(Alinha): {}\n".format(Alinha.Theta))
			Am = c.deepcopy(Alinha)
			Am.resetB()
			Am.itp = 0
			for j in range(m):
				Am.it= m*i +j
				Am.itp = Am.itp + 1
				texto.append("\t\titeracao i={},j={}\n".format(i,j))
				texto.append("\t\tTheta(Am): {}\n".format(Am.Theta))
				Smp1 = c.deepcopy(Sm) 
				a = Alinha.solver(Smp1) #gerar a ação com a política atual step 6a
				custo = Smp1.transicao(a,Prob.vqCheg) # gerar novo estado a partir da transição do atual
				erro = Am.updPol(a,Sm,Smp1,lpar)
				#step 5: gera a incerteza do cenário
				texto.append("\t\tapos atualizar Theta(Am): {}\n".format(Am.Theta))
				Stat.append([custo] +[erro] + list(Am.getStatistics()) + list(Alinha.getStatistics())) #Am.getStatistics() retorna teta #tirar o indice [1] do custo - adiciona à Stat o custo e o teta atualizado
				Stat_basis.append([custo] +[erro] + list(Am.calc_phi(Sm, lpar)))
				del(Sm)
				Sm = c.deepcopy(Smp1)
				del(Smp1)
			del(Alinha)
			Alinha = c.deepcopy(Am) #step 8: atualizar a política para a iteração i+1
			texto.append("\tTheta(Alinha): {}\n".format(Alinha.Theta))
			del(Am)
		self.adpStat(['custo'] + ['erro'] + Alinha.getStatLabels() + ['{}_curr'.format(i) for i in Alinha.getStatLabels()],Stat,n,m)
		lab = ['custo'] + ['erro'] + Alinha.getStatLabels()
		self.adpStatBasis(lab,Stat_basis)
		if self.log:
			arquivo = self.caminho + 'Log/' + 'saida.txt'
			with open(arquivo, 'w', newline='') as arq:
				arq.writelines(texto)
		del(texto)
		return Alinha

	def adpStatBasis(self,labels,Stats):
		local = self.caminho + 'Log/'
		df = pd.DataFrame(Stats)
		df.to_csv(local + 'adp_stat_basis.csv', header=labels)

	def adpStat(self,labels,Stats,n, m):
		self.StatLab = labels
		self.StatData = [[] for i in range(len(labels))] #uma lista vazia para cada label
		#print('Função adpStat:\n\t dim(Stats):{}\n\t n*m: {}'.format(len(Stats),n*m))
		#print('\n\t dim(labels):{}\n\t dim(Stats[0])n*m: {}'.format(len(labels),len(Stats[0])))
		for i in range(len(labels)): #cada label e um grafico, custo, teta1,teta2,....,teta6
			for j in range(n):
				auxn = []
				for k in range(m):
					#print('i:{}\t j:{}\t k:{}\t j*n+k: {}, Stats[j*m+k]:{}'.format(i,j,k,j*m+k,Stats[j*m+k]))
					auxn.append(Stats[j*m+k][i])
				self.StatData[i].append(auxn)
		if self.PStat:
			local = self.caminho + 'Log/'
			df = pd.DataFrame(Stats)
			df.to_csv(local + 'adp_stat.csv', header=labels)

	def graficoStat(self,idStat):
		print(len(self.StatData))
		
		k = int((len(self.StatData) -2)/2)
		print(k)
		n = len(self.StatData[idStat])
		m = len(self.StatData[idStat][0])
		s= range(n*m)
		matplotlib.pyplot.figure(figsize=(30,30))
		matplotlib.pyplot.xlabel("Iteração")
		matplotlib.pyplot.ylabel("Valor")

		local = self.caminho + 'Graficos/'
		if idStat == 0:
			y = [self.StatData[idStat][i][j] for i in range(n) for j in range(m)]
			matplotlib.pyplot.clf()
			matplotlib.pyplot.plot(s, y, label=self.StatLab[0])
			matplotlib.pyplot.title("Custo ao Longo do Tempo ")
			matplotlib.pyplot.savefig(local+'Custo.png')
		else:
			if idStat == 1:
				y = [self.StatData[idStat][i][j] for i in range(n) for j in range(m)]
				matplotlib.pyplot.clf()
				matplotlib.pyplot.plot(s, y, label=self.StatLab[1])
				matplotlib.pyplot.title("Erro ao Longo do Tempo ")
				matplotlib.pyplot.savefig(local + 'Erro.png')
			else:
				y1 = [self.StatData[idStat][i][j] for i in range(n) for j in range(m)]
				y2 = [self.StatData[idStat + k][i][j] for i in range(n) for j in range(m)]
				matplotlib.pyplot.clf()
				matplotlib.pyplot.plot(s, y1, label=self.StatLab[idStat])
				matplotlib.pyplot.plot(s, y2, label=self.StatLab[idStat+ k])
				matplotlib.pyplot.title('Coeficientes da função ' +self.StatLab[idStat]+' ao Longo do Tempo ')
				matplotlib.pyplot.savefig(local+' função '+self.StatLab[idStat]+'.png')


def teste():
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

	Prob = Problema(2,P, vfi, vbe, vroum, vrodois, lqrn, lareas, letapas,'')
	return Prob
'''
	S.imprime()
	Pol = Politica() 
	d = Pol.solver(S)
	d.imprime()
	S.transicao(d,2)
	S.imprime()

	sim = Simulador()
	[rl1,rl2,rl3,rl4] = sim.simulacao(S,Pol,2000,2)
'''


if __name__ == "__main__":

	Prob = teste()
	Prob.S.imprime()

# Instancia gerada manualmente


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
