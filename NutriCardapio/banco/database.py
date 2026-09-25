import sqlite3

CAMINHO_BANCO = "banco/nutricardapio.db"


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    return conexao