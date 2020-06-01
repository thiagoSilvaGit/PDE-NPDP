#coding: utf-8

import sys
import math
#import random
#import numpy
#import copy as c
#from numpy.random import standard_normal, normal
#from numpy import array, zeros, sqrt, shape
from Leitor.leitorXML import *
import csv
import matplotlib.pyplot
#from pprint import pprint
#import time
import NPDPADP.npdpADP as nadp
import NPDPADP.basisfunction as bf



if __name__ == "__main__":

	if len(sys.argv) > 1:
		arq_conf = sys.argv[1]
		dict_conf = LerXMLConf(arq_conf)
	else:
		print('É necessário passar o endereço do arquivo de configuração de testes como referência')
		sys.exit(1)


	lamb = nadp.switch_stpsze(dict_conf['Lambda'])
	gama = dict_conf['Gamma']
	caminho = dict_conf['Caminho']
	arqv = dict_conf['Instancia'] #carrega o arquivo da instância
	n = dict_conf['N'] #n número de iterações do Policy Iteration Algorithm
	m = dict_conf['M'] #m tamanho da simulação de Monte Carlo para convergência do valor
	it1 = dict_conf['it_sim']
	BF = dict_conf['BF']
	lbs = []
	lcoef = []

	for b in BF:
		lbs.append(bf.switch_bf(b['Nome']))
		lcoef.append(b['Coeficiente'])

	print(lbs)
	print(lcoef)


##alterar a classe problema para receber um arquivo de instância no construtor
	Prob = nadp.teste()
	Prob.S.imprime()

'''


	Prob = tadp.Problema(0,0,0,0,0,caminho) #cria Prob como um objeto da classe Problema 
	Prob.Leitura(arqv) #leitura do arquivo da instância

	t=time.time() 

	estado = tadp.Estado(Prob.lst_silos,Prob.P_ini) #cria objeto da classe Estado
	for i in range(len(estado.silos)):
		pprint (estado.silos[i].nvl) #imprime o nível (volume inicial) de cada silo

	Poli=tadp.politica(lbs,lcoef,gama,lamb,caminho) #cria Poli como um objeto da classe política
	Poli.setLog(1)
	s = tadp.simuladorTripper(caminho) #cria s como um objeto da classe simuladorTripper 
	lpar = [Prob.y1 , Prob.y2, Prob.te, Prob.ts] #lista de parâmetros do problema
	pda = tadp.ADP(caminho) #criando instância da classe ADP
	pda.setLog(1)
	apia = pda.approxPIA(Prob,Poli,n,m) #chama a função approxPIA

	pda.graficoStat(0) # é interessate adicionar os labels 
	pda.graficoStat(1)
	pda.graficoStat(2)
	pda.graficoStat(3)
	pda.graficoStat(4)
	pda.graficoStat(5)
	pda.graficoStat(6)
	pda.graficoStat(7)

	print("\n APIA: {}".format(apia.Theta))

	t = time.time()
	s.simulacao(estado, apia, lpar, it1, t)
	s.graficoTripper(estado,it1)
	s.simulacao2(estado, Poli, lpar, it2)


'''
