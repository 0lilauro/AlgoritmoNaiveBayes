import os
import csv
from time import sleep
from pprint import pprint
from modulos.etl import Etl

arquivo_saida = './dataset.csv'

if not os.path.exists(arquivo_saida):
	"""
	PROCESSO DE ETL
	"""

	# Vamos fazer a pesquisa com o dataset A
	# Neste caso os arquivos que tem spam ou spm no nome
	# sao spans, ja o resto sao hams(emails que nao sao spam).

	palavras_chaves = ['spm', 'spam']
	dataset = []
	inicio_email = 'Subject:'
	etl = Etl()
	etl.lista_arquivos = []
	etl.pesquisar_arquivos('./datasetA')

	with open(arquivo_saida, 'a') as saida:
		for dados_arquivo in etl.lista_arquivos:
			path_arquivo = dados_arquivo[0]
			nome_arquivo = dados_arquivo[1]
			classe = 'ham'

			if etl.encontrar_palavra_chave(nome_arquivo, palavras_chaves[:]):
				classe = 'spam'

			with open(path_arquivo, 'r') as email:
				linha_saida = ''
				for linha in email.readlines():
					linha_normalizada = etl.limpar_linha(linha)
					if linha.startswith(inicio_email) and linha_normalizada != '':
						linha_saida = etl.criar_linha(linha_normalizada, classe)
						break
				if etl.linha_nao_existe(dataset, linha_saida) and linha_saida:
					saida.write(linha_saida)
					dataset.append(saida)

		# Agora vamos eextrair os dados do dataset B
		# Neste, os emails estao separados em pastas diferentes entao
		# vamos simplesmente mudar o diretorio de pesquisa e fazer o carregamento
		# observe que nesse existe um try catch, por conta de nem todos os arquivos
		# estarem formatados para padrao utf e esses foram ignorados.

		etl.lista_arquivos = []
		diretorio_pesquisa = './datasetB'
		sub_diretorios = ['ham', 'spam']

		for sub_diretorio in sub_diretorios:
			etl.pesquisar_arquivos("{}/{}".format(diretorio_pesquisa, sub_diretorio))
			for dados_arquivo in etl.lista_arquivos:
				path_arquivo = dados_arquivo[0]
				nome_arquivo = dados_arquivo[1]
				try:
					with open(path_arquivo, 'r') as email:
						linha_saida = ''
						for linha in email.readlines():
							linha_normalizada = etl.limpar_linha(linha)
							if linha.startswith(inicio_email) and linha_normalizada != '':
								linha_saida = etl.criar_linha(linha_normalizada, sub_diretorio)
								break
						if etl.linha_nao_existe(dataset, linha_saida) and linha_saida:
							saida.write(linha_saida)
							dataset.append(saida)
				except:
					continue

print("Dataset processado!")
	