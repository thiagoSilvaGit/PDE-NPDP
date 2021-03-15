#coding: utf-8

import sys
import math
#import random
import numpy
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
import time



if __name__ == "__main__":

	if len(sys.argv) > 1:
		arq_conf = sys.argv[1]
		dict_conf = LerXMLConf(arq_conf)
	else:
		print('É necessário passar o endereço do arquivo de configuração de testes como referência')
		sys.exit(1)

	numpy.random.seed(1000)
	
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

	#print(lbs)
	#print(lcoef)


##alterar a classe problema para receber um arquivo de instância no construtor

	Prob = nadp.Problema(arqv)
	Prob.S.imprime()
	Poli = nadp.Politica(lbs,lcoef,gama,caminho)
	Poli.setLog(1)
	pda = nadp.ADP(caminho)
	pda.setLog(1)
	pda.setPrintStat(1)
	t = time.time()
	apia = pda.approxPIA(Prob,Poli,n,m) #chama a função approxPIA


	pda.graficoStat(0) # é interessate adicionar os labels 
	pda.graficoStat(1)
	for k in range(len(lbs)):
		pda.graficoStat(2+k)


	print("\n APIA: {}".format(apia.Theta))

	total = time.time() - t
	print("\n Tempo de treinameto: {}".format(total))

	sim = nadp.Simulador()
	sim.simulacao(Prob, apia, it1,caminho)
