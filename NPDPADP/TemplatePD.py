#coding: utf-8
#from gurobipy import *
import math
from io import StringIO
import numpy as np
#from scipy.stats import norm

fxsd = "esquema_entrada.xsd"


# Modelo


# Definicao das Classes

# Classe Problema
class Problema:
	''' Classe com os parametros que definem a instancia do problema
		Objetivo: Gerenciar a instância do problema
		Métodos Obrigatórios: 
				 - Leitura
				 - ImprimeResultados
				 - SalvaResultados
		Variáveis Obrigatórias:
				 - Arquivo de entrada
				 - Nome da Instância			

	'''
	def __init__(self, InstPar):
		'''
			Construtor
			\par InstPar - Lista de parametros das instancia
			DEVE SER SOBRESCRITO  
		'''  
		return 0

	def Leitura(self, ArqEntrada):
		'''
			Metodo para carregamento de dados das instancias
			\par ArqEntrada  - Nome do arquivo de entrada
			DEVE SER SOBRESCRITO
		'''
		return 0 

	def ImprimeResultados(self):
		'''
			Metodo para impressao de resultados da analise
			DEVE SER SOBRESCRITO
		'''
		return 0 

	def SalvaResultados(self, ArqSaida):
		'''
			Metodo para escrita detalhada de resultados da analise
			\par ArqSaida  - Nome do arquivo de saida
			DEVE SER SOBRESCRITO
		'''
		return 0 
  
 
# Classe Gerador
class Gerador:
	''' Geradora de instancias para as classes do problema
		Objetivos: 1) Gerar estado inicial
				   2) Dar suporte para a classe GeraIncerteza
 
		Métodos Obrigatórios: 
				 - EstadoZero()
		Variáveis Obrigatórias:
	'''

	def __init__(self, ParGen):
		'''
		   Construtor
		   \par ParGen - Lista de parametros para geracao do estado
		   DEVE SER SOBRESCRITO
		'''  
		return 0

# Classe Estado
class Estado:
	''' Classe que representa o estado do sistema
		Objetivos: 1) Armazenar as variáveis de estado
				   2) Realizar transicao

 
		Métodos Obrigatórios: 
				 - Transicao()
				 - imprime()
		Variáveis Obrigatórias:
				 - estagio - estagio atual do sistema 
	'''
	estagio = 0
	def __init__(self, ParEst):
		'''
		   Construtor
		   \par ParEst - Lista de parametros para inicializacao do estado
		   DEVE SER SOBRESCRITO
		'''  
		return 0
			
	def imprime(self):
		'''
		   Metodo que imprime as informacoes do estado
		   DEVE SER SOBRESCRITO
		'''
		return 0

	def transicao(self,Dec,ParInc = []):
		'''
		   Metodo que realiza a transicao do estado
		   \par Dec - Instancia da classe decisao
		   \par ParInc - Lista de parametros para geracao de incerteza
		   \return ValorAfterUpdate
			NAO PODE SER SOBRESCRITO
		'''  
		Incerteza = GeraIncerteza(self,Dec,self.estagio,ParInc)
		Incerteza.geracao()
		# Passagem de estagio
		self.estagio = self.estagio+1
		ValorAfterUpdate = self.Atualizar(Incerteza)
		return ValorAfterUpdate

	def Atualizar(self,Incerteza):
		'''
		   Metodo que atualiza as informacoes do estado apos a geracao de incerteza  dentro do processo de transicao
		   \par Incerteza - Instacia da classe incerteza apos a geracao
		   \return ValorAfterUpdate
		   DEVE SER SOBRESCRITO
		'''  
		return 0

	   


# Classe Decisao 		
class Decisao:
	''' Classe que organiza a decisão tomada pela politica
		Objetivos: 1) padronizar o formato da decisao
		Métodos Obrigatórios: 
				  - def imprime()
		Variáveis Obrigatórias:
				   
	'''

	def __init__(self, ParDec):
		'''
		   Construtor
		   \par ParDec - Lista de parametros resultantes do metodo de solucao
		   DEVE SER SOBRESCRITO
		'''  
		return 0 
	def imprime(self):
		'''
		   Metodo que imprime as informacoes da decisao
		   DEVE SER SOBRESCRITO
		'''
		return 0 
		
  
	
# Classe GeraIncerteza 		
class GeraIncerteza:
	''' Classe que gera a incerteza do problema
		Objetivos: 1) Gerar incerteza
		Métodos Obrigatórios: 
				  - geracao()
				  - CalcValor(self): 
		Variáveis Obrigatórias:
				  
				   
	'''


	def __init__(self, vEstado, vDecisao,vEstagio,ParInc):
		'''
		   Construtor
		   \par vEstado - instancia da classe Estado
		   \par vDecisao - instancia da classe Decisao
		   \par vEstagio - inteiro com a informação do estagio atual
		   \par ParInc - lista com parâmetros para realizacao da incerteza
	  
		   DEVE SER SOBRESCRITO
		'''  
		return 0

	def geracao(self):
		'''
		   Metodo que gera incerteza propriamente dita
		   DEVE SER SOBRESCRITO
		'''
		return 0

	def CalcValor(self):
		'''
		   Calcula Valor dos custos apos a realizacao da incerteza
		   DEVE SER SOBRESCRITO'
		'''
		return ret									
		   
# Classe Politica
class Politica:
	''' Classe que representa uma politica apra a solucao do problema
		Objetivos: 1) Resolver o subproblema
				   2) Realizar o treinamento se necessário
		Métodos Obrigatórios: 
				  - solver() 
		Variáveis Obrigatórias:
				   
	'''
	def __init__(self, ParPol):
		'''
		   Construtor
		   \par ParPol - lista com parâmetros para a politica
  
		   DEVE SER SOBRESCRITO
		'''  

	def solver(self,EstX):
		'''
		   Metodo de solucao
		   \par EstX - instancia da classe estado
		   \return - deve retornar uma instancia da classe decisao
  
		   DEVE SER SOBRESCRITO
		'''  
		return d

class Simulador:
	''' Classe que simula a dinâmica do processo a partir de um estado inicial e para uma política específica
		Objetivos: 1) Simular o processo
				   2) Coletar estatísticas
		Métodos Obrigatórios: 
				  - simulacao(self, Est, Pol, niter, lpar):
		Variáveis Obrigatórias:
				   
	'''
	def simulacao(self, EstX, Pol, niter, lpar):
		'''
		   Metodo de simulucao
		   \par EstX - instancia da classe estado
		   \par Pol - Política
		   \niter - Número de iteações	  
		   \return - deve retornar uma instancia da classe decisao
  
		   DEVE SER SOBRESCRITO
		'''  
		return 0

class Trainer:

	''' Classe que realiza o treinamento de políticas a partir de algoritmo implementado no método approxPD
		Objetivos: 1) Treinar política
				   2) Coletar estatísticas
		Métodos Obrigatórios: 
				  - approxDP(P,B,A,n,m,atualizaPolitica):
		Variáveis Obrigatórias:'''

	def approxDP(P,B,A,n,m,atualizaPolitica):
		return 0


