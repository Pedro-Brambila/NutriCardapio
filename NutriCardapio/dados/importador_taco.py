import sqlite3
import pandas as pd
from pathlib import Path


CAMINHO_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = CAMINHO_PROJETO / "banco" / "nutricardapio.db"
CAMINHO_DADOS = Path(__file__).resolve().parent


def conectar_banco():
    return sqlite3.connect(CAMINHO_BANCO)


def encontrar_excel():
    arquivos = list(CAMINHO_DADOS.glob("*.xlsx")) + list(CAMINHO_DADOS.glob("*.xls"))

    if not arquivos:
        print("Nenhum arquivo Excel encontrado na pasta dados.")
        return None

    return arquivos[0]


def numero(valor):
    """
    Converte valores da TACO para número.

    Na TACO, 'Tr' significa traço/quantidade muito pequena.
    Como nosso banco usa números, vamos representar 'Tr' como 0
    nesta primeira versão.
    """
    if pd.isna(valor):
        return None

    if isinstance(valor, str):
        valor = valor.strip()

        if valor.lower() == "tr":
            return 0.0

        valor = valor.replace(",", ".")

    try:
        return float(valor)
    except (ValueError, TypeError):
        return None


def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            fonte TEXT NOT NULL,
            unidade_base TEXT NOT NULL DEFAULT 'g',
            quantidade_base REAL NOT NULL DEFAULT 100,

            energia_kcal REAL,
            proteina_g REAL,
            carboidrato_g REAL,
            gordura_g REAL,
            fibra_g REAL,

            calcio_mg REAL,
            ferro_mg REAL,
            sodio_mg REAL,
            potassio_mg REAL,
            magnesio_mg REAL,
            fosforo_mg REAL,

            vitamina_a_mcg REAL,
            vitamina_c_mg REAL,

            UNIQUE(nome, fonte)
        )
    """)

    conexao.commit()
    conexao.close()


def importar_taco():
    arquivo = encontrar_excel()

    if arquivo is None:
        return

    print(f"Arquivo encontrado: {arquivo.name}")

    # A primeira planilha é a tabela principal da TACO
    df = pd.read_excel(
        arquivo,
        sheet_name="CMVCol taco3",
        header=None
    )

    conexao = conectar_banco()
    cursor = conexao.cursor()

    importados = 0
    ignorados = 0

    # Os alimentos começam na linha 4 do Excel.
    # No pandas, isso corresponde ao índice 4.
    for indice in range(4, len(df)):

        numero_alimento = df.iloc[indice, 0]
        nome = df.iloc[indice, 1]

        # Ignora linhas que não representam alimentos
        if pd.isna(numero_alimento) or pd.isna(nome):
            continue

        nome = str(nome).strip()

        if not nome:
            continue

        # Verifica se o primeiro campo realmente é um número
        try:
            int(float(numero_alimento))
        except (ValueError, TypeError):
            continue

        # Colunas da TACO
        energia = numero(df.iloc[indice, 3])
        proteina = numero(df.iloc[indice, 5])
        gordura = numero(df.iloc[indice, 6])
        carboidrato = numero(df.iloc[indice, 8])
        fibra = numero(df.iloc[indice, 9])

        calcio = numero(df.iloc[indice, 11])
        magnesio = numero(df.iloc[indice, 12])
        fosforo = numero(df.iloc[indice, 15])
        ferro = numero(df.iloc[indice, 16])
        sodio = numero(df.iloc[indice, 17])
        potassio = numero(df.iloc[indice, 18])

        # RAE = Equivalente de atividade de retinol
        # É a coluna que vamos usar como vitamina A.
        vitamina_a = numero(df.iloc[indice, 23])

        vitamina_c = numero(df.iloc[indice, 28])

        cursor.execute("""
            INSERT OR IGNORE INTO alimentos (
                nome,
                fonte,
                unidade_base,
                quantidade_base,
                energia_kcal,
                proteina_g,
                carboidrato_g,
                gordura_g,
                fibra_g,
                calcio_mg,
                ferro_mg,
                sodio_mg,
                potassio_mg,
                magnesio_mg,
                fosforo_mg,
                vitamina_a_mcg,
                vitamina_c_mg
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nome,
            "TACO 4ª Edição",
            "g",
            100,
            energia,
            proteina,
            carboidrato,
            gordura,
            fibra,
            calcio,
            ferro,
            sodio,
            potassio,
            magnesio,
            fosforo,
            vitamina_a,
            vitamina_c
        ))

        if cursor.rowcount == 1:
            importados += 1
        else:
            ignorados += 1

    conexao.commit()
    conexao.close()

    print()
    print("===================================")
    print("IMPORTAÇÃO CONCLUÍDA")
    print("===================================")
    print(f"Alimentos importados: {importados}")
    print(f"Alimentos já existentes: {ignorados}")
    print("Fonte: TACO 4ª Edição")
    print("Base nutricional: 100 g")
    print("===================================")


if __name__ == "__main__":
    criar_tabela()
    importar_taco()