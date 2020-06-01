# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import math
import numpy as np
import copy as c
from Leitor.leitorXML import *
from NPDPADP import npdpADP as nadp


# Classe Gerador
class Gerador:

	def __init__(self, *args, **kwargs):
				# vna, vne, nproj,prec1,prec2,vfi,vbe,ifile):

		if len(args) ==1:
			geraDict = LerXMLGen(args[0])
			self.nAreas = int(geraDict['nA'])
			self.nEtapas = int(geraDict['nE'])
			self.nProj = int(geraDict['nProj'])
			self.lrec = [float(geraDict['pRec1']),float(geraDict['pRec2'])]
			self.lro = [float(geraDict['vro1']),float(geraDict['vro2'])]
			self.vqCheg = int(geraDict['maxCheg'])
			self.vfi = float(geraDict['vfi'])
			self.vbe = float(geraDict['vbe'])
			self.instFile = str(geraDict['fileName'])
			self.caminho = str(geraDict['caminho'])

		else:
			if (len(args) > 9) and (len(args) < 13):
				self.nAreas = int(args[0])
				self.nEtapas = int(args[1])
				self.nProj = int(args[2])
				self.vqCheg = int(args[3])
				self.lrec = [float(args[4]),float(args[5])]
				self.lro = [float(args[6]), float(args[7])]
				self.vfi = float(args[8])
				self.vbe = float(args[9])
				if len(args) == 12:
					self.instFile = str(args[10])
					self.caminho = str(args[11])
			else:
				print('Gerador(): Erro na passagem de parametros')
				sys.exit(1)

	def geraInst(self, w):
		lareas = self.geraAreas()
		letapas = self.geraEtapas()
		qrnr = self.geraRecNRen()
		P =[]
		for i in range(self.nProj):
			p = self.geraProjeto(i, letapas, lareas, qrnr,0)
			P.append(p)

		inst = [P, self.vfi, self.vbe, self.lro,self.vqCheg, qrnr, lareas, letapas]
		if w:
			self.writeIns(inst)

		return inst


	def writeIns(self,linst):
		#lProj, vfi, vbe, vroum, vrodois,
		arq = open( self.caminho + self.instFile + '.xml', 'w')
		texto = []
		texto.append('<?xml version="1.0" encoding="UTF-8"?>\n')
		texto.append('<NPDP_instGen Arq_name = "'+ self.instFile + '.xml">\n')

		texto.append('\t<Caminho>'+ self.caminho + '</Caminho>\n')
		texto.append('\t<Problema>\n')
		texto.append('\t\t<nA>'+str(self.nAreas)+'</nA>\n')
		texto.append('\t\t<nE>'+str(self.nEtapas)+'</nE>\n')
		texto.append('\t\t<maxCheg>'+str(self.vqCheg)+'</maxCheg>\n')
		texto.append('\t\t<vfi>'+str(self.vfi)+'</vfi>\n')
		texto.append('\t\t<vbe>'+str(self.vbe)+'</vbe>\n')
		texto.append('\t\t<ro1>'+str(linst[3][0])+'</ro1>\n')
		texto.append('\t\t<ro2>'+str(linst[3][1])+'</ro2>\n')
		texto.append('\t\t<qRec>' + str(linst[5]) + '</qRec>\n')

		for p in linst[0]:
			texto = texto + self.writeProj(p)

		texto.append('\t</Problema>\n')
		texto.append('</NPDP_instGen>\n')
		arq.writelines(texto)
		arq.close()
		return 0
	def writeProj(self,p):
		texto = []
		texto.append('\t\t<Projeto>\n')
		texto.append('\t\t\t<nome>' + str(p.nome) + '</nome>\n')

		for me in p.modos:
			texto = texto + self.writeModos(me)

		texto.append('\t\t\t<Mx>' + str(p.par[0]) + '</Mx>\n')
		texto.append('\t\t\t<mn>' + str(p.par[1]) + '</mn>\n')
		texto.append('\t\t\t<a>' + str(p.par[2]) + '</a>\n')
		texto.append('\t\t\t<pk>' + str(p.par[3]) + '</pk>\n')
		texto.append('\t\t\t<mu>' + str(p.par[4]) + '</mu>\n')
		texto.append('\t\t\t<desvp>' + str(p.par[5]) + '</desvp>\n')
		texto.append('\t\t\t<div>' + str(p.div) + '</div>\n')
		for i in p.tempo:
			texto = texto + ['\t\t\t<tempo>' + str(i) + '</tempo>\n']

		texto.append('\t\t\t<cmax>' + str(p.cmax) + '</cmax>\n')
		texto.append('\t\t\t<area>' + str(p.area) + '</area>\n')
		texto.append('\t\t\t<etapa>' + str(p.etapa) + '</etapa>\n')
		texto.append('\t\t\t<tCheg>' + str(p.tCheg) + '</tCheg>\n')
		texto.append('\t\t</Projeto>\n')
		return texto
	def writeModos(self,me):
		texto = []
		texto.append('\t\t\t<Modos>\n')
		for m in me:
			texto = texto + self.writeModo(m)
		texto.append('\t\t\t</Modos>\n')
		return texto
	def writeModo(self,m):
		texto = []
		texto.append('\t\t\t\t<Modo>\n')
		texto.append('\t\t\t\t\t<nome>' + str(m.nome) + '</nome>\n')
		texto.append('\t\t\t\t\t<prob>' + str(m.prob) + '</prob>\n')
		texto.append('\t\t\t\t\t<probAtr>' + str(m.probAtr) + '</probAtr>\n')
		texto.append('\t\t\t\t\t<deltap>' + str(m.deltap) + '</deltap>\n')
		texto.append('\t\t\t\t\t<nrn>' + str(m.nrn) + '</nrn>\n')
		texto.append('\t\t\t\t\t<deltat>' + str(m.deltat) + '</deltat>\n')
		texto.append('\t\t\t\t</Modo>\n')
		return texto

	def geraAreas(self):
		# Gerando areas
		A = []
		# Nomeando a area
		for a in range(self.nAreas):
			anome = 'A' + str(a + 1)
			A.append(anome)
		return A

	# Gerando os recursos do modelo: 200 multiplicando uma funcao aleatoria uniforme e adicionando 50
	def geraRecNRen(self):
		return self.lrec[1] * np.random.uniform() + self.lrec[1]

	# Gerando as etapas do modelo
	def geraEtapas(self):
		return range(self.nEtapas)

	# Gerando os projetos do modelo
	def geraProjeto(self, pid, Etapas, Areas, qrnr, estagio):
		# Nome dos projetos
		vnome = 'p' + str(pid)
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
		varea = Areas[np.random.randint(0, len(Areas) - 1)]

		for ie in range(netapas):
			nt = np.random.randint(1, 4)
			ltempo.append(nt)
			# Lista de tempos recebendo valor
			tempo += nt
		for ie in range(netapas):
			quant = np.random.randint(1, 3)
			imodo = self.geraModo(quant, desvp, tempo, qrnr)
			# As necessidades de recurso sendo atribuidas
			totalCost += imodo[0].nrn * ltempo[ie]
			lmodos.append(imodo)

		# Os valores maximo e minimo esperado recebem um valor a partir de uma distribuicao uniforme multiplicada pelo custo total
		mn = (np.random.uniform() + 1) * totalCost
		Mx = mn + np.random.uniform(2, 10) * totalCost
		moda = tempo - 2 + np.random.randint(1, 3)
		# Parametro de forma
		pk = np.random.randint(2, 4)
		vpk = ((pk - 1) / pk) ** (1 / pk)
		# Parametro de escala
		a = moda / vpk
		# Lista de parametros dos projetos recebe os valores
		lpar = [Mx, mn, a, pk, 0, desvp]
		vdiv = np.random.binomial(1, 0.5)
		# so pode haver congelamento maximo se o projeto for divisivel
		if (vdiv == 1):
			vcmax = 1 + math.floor(0.3 * np.random.uniform() * tempo)
		else:
			vcmax = 0
		p1 = nadp.Projeto(lmodos, lpar, vdiv, ltempo, vcmax, varea, vetapa, vnome, estagio)
		return p1

	# Gerando os modos do modelo
	def geraModo(self, quant, desv, tempo, qrnr):
		M = []
		# Parametros dos modos: Probabilidades e necessidade de recursos
		prob1 = 0.8 * np.random.uniform()
		prob2 = np.random.uniform(0.0, 0.15)
		vdelta = np.random.uniform(1, 3) * (desv / tempo)
		lnrn = 0.2 * np.random.uniform() * qrnr
		vdeltat = 1

		# Sempre e criado o modo 'continuar'
		m1 = nadp.Modo(prob1, prob2, vdelta, lnrn, vdeltat, "Continuar")
		M.append(m1)
		# Se forem dois o numero de modos, cria-se o 'melhorar'
		if (quant > 1):
			prob = np.random.uniform(prob1, 1.0)
			vdelta1 = np.random.uniform(1, 2) * vdelta
			vdeltat = 1
			lnrn1 = np.random.uniform(1, 3) * lnrn
			vmean = np.random.uniform
			m2 = nadp.Modo(prob, prob2, vdelta1, lnrn, vdeltat, "Melhorar")
			M.append(m2)
		# Se forem tres, cria-se o 'acelerar'
		if (quant > 2):
			prob2 = np.random.uniform(0.0, prob2)
			lnrn1 = np.random.uniform(1, 3) * lnrn
			vdeltat1 = 2
			m3 = nadp.Modo(prob1, prob2, vdelta1 * (tempo / (tempo - (vdeltat1 - vdeltat))), lnrn1, vdeltat1, "Acelerar")
			M.append(m3)
		# Se for mais de 3, nao cria-se mais modos
		if (quant > 3):
			print('Serao gerados apenas 3 modos') # hahahahahahahaahahahaha
		return M


if __name__ == "__main__":


	if len(sys.argv) > 1:
		arq_gen = sys.argv[1]

	else:
		print('É necessário passar o endereço do arquivo de configuração de testes como referência')
		sys.exit(1)

	G = Gerador(arq_gen)
	G.geraInst(1)

'''G = nadp.Gerador(3,3)
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
'''
