from banco.database import conectar_banco


def criar_tabela_alimentos():
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


def pesquisar_alimento(nome):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
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
        FROM alimentos
        WHERE nome LIKE ?
        ORDER BY nome
    """, (f"%{nome}%",))

    resultados = cursor.fetchall()

    conexao.close()

    alimentos = []

    for resultado in resultados:
        alimentos.append({
            "id": resultado[0],
            "nome": resultado[1],
            "fonte": resultado[2],
            "unidade_base": resultado[3],
            "quantidade_base": resultado[4],
            "energia_kcal": resultado[5],
            "proteina_g": resultado[6],
            "carboidrato_g": resultado[7],
            "gordura_g": resultado[8],
            "fibra_g": resultado[9],
            "calcio_mg": resultado[10],
            "ferro_mg": resultado[11],
            "sodio_mg": resultado[12],
            "potassio_mg": resultado[13],
            "magnesio_mg": resultado[14],
            "fosforo_mg": resultado[15],
            "vitamina_a_mcg": resultado[16],
            "vitamina_c_mg": resultado[17]
        })

    return alimentos