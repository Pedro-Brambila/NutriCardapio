import sqlite3
from pathlib import Path

# Caminho absoluto baseado na localização deste arquivo (banco/database.py),
# assim funciona não importa de onde o programa seja executado
# (terminal local, Streamlit Cloud, outro PC, etc.).
CAMINHO_BANCO = Path(__file__).resolve().parent / "nutricardapio.db"


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    return conexao