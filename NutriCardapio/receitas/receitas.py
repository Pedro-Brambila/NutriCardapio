from banco.database import conectar_banco


def criar_tabelas_receitas():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            porcoes INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredientes_receita (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receita_id INTEGER NOT NULL,
            alimento_id INTEGER NOT NULL,
            quantidade_g REAL NOT NULL,

            FOREIGN KEY (receita_id)
                REFERENCES receitas(id),

            FOREIGN KEY (alimento_id)
                REFERENCES alimentos(id)
        )
    """)

    conexao.commit()
    conexao.close()


def calcular_nutrientes(nome, quantidade):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            nome,
            fonte,
            quantidade_base,
            energia_kcal,
            proteina_g,
            carboidrato_g,
            gordura_g,
            fibra_g
        FROM alimentos
        WHERE nome LIKE ?
        ORDER BY nome
        LIMIT 1
    """, (f"%{nome}%",))

    alimento = cursor.fetchone()

    conexao.close()

    if alimento is None:
        return None

    fator = quantidade / alimento[2]

    return {
        "nome": alimento[0],
        "fonte": alimento[1],
        "quantidade": quantidade,
        "energia_kcal": alimento[3] * fator,
        "proteina_g": alimento[4] * fator,
        "carboidrato_g": alimento[5] * fator,
        "gordura_g": alimento[6] * fator,
        "fibra_g": alimento[7] * fator
    }


def calcular_receita(ingredientes):
    total = {
        "energia_kcal": 0,
        "proteina_g": 0,
        "carboidrato_g": 0,
        "gordura_g": 0,
        "fibra_g": 0
    }

    for nome, quantidade in ingredientes:

        resultado = calcular_nutrientes(
            nome,
            quantidade
        )

        if resultado is None:
            print(f"Alimento não encontrado: {nome}")
            continue

        total["energia_kcal"] += resultado["energia_kcal"]
        total["proteina_g"] += resultado["proteina_g"]
        total["carboidrato_g"] += resultado["carboidrato_g"]
        total["gordura_g"] += resultado["gordura_g"]
        total["fibra_g"] += resultado["fibra_g"]

    return total


def salvar_receita(nome, porcoes, ingredientes):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO receitas (nome, porcoes)
        VALUES (?, ?)
    """, (nome, porcoes))

    receita_id = cursor.lastrowid

    for ingrediente in ingredientes:

        alimento_id = ingrediente["id"]
        quantidade = ingrediente["quantidade"]

        cursor.execute("""
            INSERT INTO ingredientes_receita (
                receita_id,
                alimento_id,
                quantidade_g
            )
            VALUES (?, ?, ?)
        """, (
            receita_id,
            alimento_id,
            quantidade
        ))

    conexao.commit()
    conexao.close()

    return receita_id
def listar_receitas():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, porcoes
        FROM receitas
        ORDER BY nome
    """)

    receitas = cursor.fetchall()

    conexao.close()

    return receitas


def buscar_receita(receita_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.porcoes,
            a.id,
            a.nome,
            a.fonte,
            ir.quantidade_g,
            a.quantidade_base,
            a.energia_kcal,
            a.proteina_g,
            a.carboidrato_g,
            a.gordura_g,
            a.fibra_g
        FROM receitas r
        JOIN ingredientes_receita ir
            ON r.id = ir.receita_id
        JOIN alimentos a
            ON a.id = ir.alimento_id
        WHERE r.id = ?
        ORDER BY ir.id
    """, (receita_id,))

    resultados = cursor.fetchall()

    conexao.close()

    if not resultados:
        return None

    receita = {
        "id": resultados[0][0],
        "nome": resultados[0][1],
        "porcoes": resultados[0][2],
        "ingredientes": []
    }

    total = {
        "energia_kcal": 0,
        "proteina_g": 0,
        "carboidrato_g": 0,
        "gordura_g": 0,
        "fibra_g": 0
    }

    for resultado in resultados:

        quantidade = resultado[6]
        quantidade_base = resultado[7]

        fator = quantidade / quantidade_base

        energia = resultado[8] * fator
        proteina = resultado[9] * fator
        carboidrato = resultado[10] * fator
        gordura = resultado[11] * fator
        fibra = resultado[12] * fator

        ingrediente = {
            "id": resultado[3],
            "nome": resultado[4],
            "fonte": resultado[5],
            "quantidade": quantidade,
            "energia_kcal": energia,
            "proteina_g": proteina,
            "carboidrato_g": carboidrato,
            "gordura_g": gordura,
            "fibra_g": fibra
        }

        receita["ingredientes"].append(ingrediente)

        total["energia_kcal"] += energia
        total["proteina_g"] += proteina
        total["carboidrato_g"] += carboidrato
        total["gordura_g"] += gordura
        total["fibra_g"] += fibra

    receita["total"] = total

    return receita
def atualizar_receita(receita_id, nome, porcoes, ingredientes):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE receitas
            SET nome = ?, porcoes = ?
            WHERE id = ?
        """, (nome, porcoes, receita_id))

        cursor.execute("""
            DELETE FROM ingredientes_receita
            WHERE receita_id = ?
        """, (receita_id,))

        for ingrediente in ingredientes:
            cursor.execute("""
                INSERT INTO ingredientes_receita (
                    receita_id,
                    alimento_id,
                    quantidade_g
                )
                VALUES (?, ?, ?)
            """, (
                receita_id,
                ingrediente["id"],
                ingrediente["quantidade"]
            ))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


def excluir_receita(receita_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            DELETE FROM ingredientes_receita
            WHERE receita_id = ?
        """, (receita_id,))

        cursor.execute("""
            DELETE FROM receitas
            WHERE id = ?
        """, (receita_id,))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()