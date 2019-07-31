
import os 
import re
import csv
import random

class Etl:
	
	"""
	Construtor da classe

	adiciona o atrivo lista_arquivos como atributo privado
	"""
	def __init__(self):
		self._lista_arquivos = []

	# GETTERS
	@property
	def lista_arquivos(self):
		return self._lista_arquivos

	# SETTERS
	@lista_arquivos.setter
	def lista_arquivos(self, value):
		self._lista_arquivos = value

	
	"""
	Esse metodo serve para criar uma lista de arquivos em um diretorio.

	parametro diretorio - onde vao ser proucurados os arquivos

	retorno list - com os arquivos listados	
	"""	
	def pesquisar_arquivos(self, diretorio):
		for item in os.listdir(diretorio):
			path = "{}/{}".format(diretorio, item)
			if (os.path.isfile(path)):
				dados = [path, item]
				self._lista_arquivos.append(dados)
			else:
				self.pesquisar_arquivos(path)

	"""
	Esse metodo e utilizado para limpar strings e tirar caracteres indesejados.
	Deixa apenas todo o conteudo após o texto de 'Subject:' que possuí 8 
	caracteres e remove o ultimo elemento da linha que é o caracter '\n' que 
	significa quebra de linha. Além de retirar os espaços repetidos e os 
	espaços em branco no inicio e no final da string.

	parametro string linha - linha a ser tratada

	retorno string linha - linha com o tratamento	
	"""	
	def limpar_linha(self, linha):
		linha = re.sub(r'[^a-zA-Z\s]', '', linha)[8:-1]
		linha = re.sub(' +', ' ', linha).strip()
		return linha


	"""
	Esse e um metodo recursivo que proucura a ocorrencia de palavras chaves de uma lista em um
	texto, sem necessariamente 'percorrela'.


	parametro list palavras - uma lista com palavras chaves para serem proucuradas no texto.

	parametro string texto - uma linha de texto que pode ou nao encontrar as palavras

	retorno boolean - se alguma palavra da lista foi encontrada no texto
	"""
	def encontrar_palavra_chave(self, texto, palavras):
		if(len(palavras) > 0):
			palavra_teste = palavras[-1]
			palavras.pop()
			return bool(texto.lower().find(palavra_teste) >= 0 or self.encontrar_palavra_chave(texto, palavras))
		else:
			return False


	"""	
	Esse metodo testa se a linha em questao ja foi registrada em um dataset(lista)

	
	parametro list lista_linhas - lista de todas as linhas registradas

	parametro string linha - linha a ser testada

	retorno boolean - retorna se existe ou nao a lista na linha
	"""
	def linha_nao_existe(self, lista_linhas, linha):
		for item in lista_linhas:
			if item == linha:
				return False
		return True


	"""	
	Esse metodo formata parametros para serem adicionados como uma linha no final de um
	arquivo csv onde sera o dataset do test.

	
	parametro string classe - titulo da classe a ser testaada

	parametro string texto - linha do titulo do email 

	retorno string - linha para ser adicionada no arquivo csv.
	"""
	def criar_linha(self, texto, classe): 
		return '"{}","{}"\n'.format(texto, classe)
