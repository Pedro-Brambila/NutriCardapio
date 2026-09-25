from banco.database import conectar_banco


def criar_tabelas_cardapios():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cardapios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS refeicoes_cardapio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cardapio_id INTEGER NOT NULL,
            nome TEXT NOT NULL,

            FOREIGN KEY (cardapio_id)
                REFERENCES cardapios(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alimentos_cardapio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            refeicao_id INTEGER NOT NULL,
            alimento_id INTEGER NOT NULL,
            quantidade_g REAL NOT NULL,

            FOREIGN KEY (refeicao_id)
                REFERENCES refeicoes_cardapio(id),

            FOREIGN KEY (alimento_id)
                REFERENCES alimentos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receitas_cardapio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            refeicao_id INTEGER NOT NULL,
            receita_id INTEGER NOT NULL,
            porcoes REAL NOT NULL DEFAULT 1,

            FOREIGN KEY (refeicao_id)
                REFERENCES refeicoes_cardapio(id),

            FOREIGN KEY (receita_id)
                REFERENCES receitas(id)
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_cardapio(nome, refeicoes):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO cardapios (nome)
            VALUES (?)
        """, (nome,))

        cardapio_id = cursor.lastrowid

        for refeicao in refeicoes:

            cursor.execute("""
                INSERT INTO refeicoes_cardapio (
                    cardapio_id,
                    nome
                )
                VALUES (?, ?)
            """, (
                cardapio_id,
                refeicao["nome"]
            ))

            refeicao_id = cursor.lastrowid

            for alimento in refeicao["alimentos"]:

                cursor.execute("""
                    INSERT INTO alimentos_cardapio (
                        refeicao_id,
                        alimento_id,
                        quantidade_g
                    )
                    VALUES (?, ?, ?)
                """, (
                    refeicao_id,
                    alimento["id"],
                    alimento["quantidade"]
                ))

            for receita in refeicao["receitas"]:

                cursor.execute("""
                    INSERT INTO receitas_cardapio (
                        refeicao_id,
                        receita_id,
                        porcoes
                    )
                    VALUES (?, ?, ?)
                """, (
                    refeicao_id,
                    receita["id"],
                    receita["porcoes"]
                ))

        conexao.commit()

        return cardapio_id

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


def listar_cardapios():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM cardapios
        ORDER BY nome
    """)

    cardapios = cursor.fetchall()

    conexao.close()

    return cardapios
def buscar_cardapio(cardapio_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM cardapios
        WHERE id = ?
    """, (cardapio_id,))

    cardapio_resultado = cursor.fetchone()

    if cardapio_resultado is None:
        conexao.close()
        return None

    cardapio = {
        "id": cardapio_resultado[0],
        "nome": cardapio_resultado[1],
        "refeicoes": []
    }

    cursor.execute("""
        SELECT id, nome
        FROM refeicoes_cardapio
        WHERE cardapio_id = ?
        ORDER BY id
    """, (cardapio_id,))

    refeicoes = cursor.fetchall()

    for refeicao_resultado in refeicoes:

        refeicao = {
            "id": refeicao_resultado[0],
            "nome": refeicao_resultado[1],
            "alimentos": [],
            "receitas": []
        }

        cursor.execute("""
            SELECT
                ac.alimento_id,
                a.nome,
                a.fonte,
                ac.quantidade_g
            FROM alimentos_cardapio ac
            JOIN alimentos a
                ON a.id = ac.alimento_id
            WHERE ac.refeicao_id = ?
            ORDER BY ac.id
        """, (refeicao["id"],))

        alimentos = cursor.fetchall()

        for alimento in alimentos:
            refeicao["alimentos"].append({
                "id": alimento[0],
                "nome": alimento[1],
                "fonte": alimento[2],
                "quantidade": alimento[3]
            })

        cursor.execute("""
            SELECT
                rc.receita_id,
                r.nome,
                rc.porcoes
            FROM receitas_cardapio rc
            JOIN receitas r
                ON r.id = rc.receita_id
            WHERE rc.refeicao_id = ?
            ORDER BY rc.id
        """, (refeicao["id"],))

        receitas = cursor.fetchall()

        for receita in receitas:
            refeicao["receitas"].append({
                "id": receita[0],
                "nome": receita[1],
                "porcoes": receita[2]
            })

        cardapio["refeicoes"].append(refeicao)

    conexao.close()

    return cardapio


def atualizar_cardapio(cardapio_id, nome, refeicoes):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE cardapios
            SET nome = ?
            WHERE id = ?
        """, (nome, cardapio_id))

        # Busca as refeições antigas
        cursor.execute("""
            SELECT id
            FROM refeicoes_cardapio
            WHERE cardapio_id = ?
        """, (cardapio_id,))

        refeicoes_antigas = cursor.fetchall()

        # Remove os itens das refeições antigas
        for refeicao in refeicoes_antigas:

            refeicao_id = refeicao[0]

            cursor.execute("""
                DELETE FROM alimentos_cardapio
                WHERE refeicao_id = ?
            """, (refeicao_id,))

            cursor.execute("""
                DELETE FROM receitas_cardapio
                WHERE refeicao_id = ?
            """, (refeicao_id,))

        # Remove as refeições antigas
        cursor.execute("""
            DELETE FROM refeicoes_cardapio
            WHERE cardapio_id = ?
        """, (cardapio_id,))

        # Cria novamente as refeições
        for refeicao in refeicoes:

            cursor.execute("""
                INSERT INTO refeicoes_cardapio (
                    cardapio_id,
                    nome
                )
                VALUES (?, ?)
            """, (
                cardapio_id,
                refeicao["nome"]
            ))

            refeicao_id = cursor.lastrowid

            for alimento in refeicao["alimentos"]:

                cursor.execute("""
                    INSERT INTO alimentos_cardapio (
                        refeicao_id,
                        alimento_id,
                        quantidade_g
                    )
                    VALUES (?, ?, ?)
                """, (
                    refeicao_id,
                    alimento["id"],
                    alimento["quantidade"]
                ))

            for receita in refeicao["receitas"]:

                cursor.execute("""
                    INSERT INTO receitas_cardapio (
                        refeicao_id,
                        receita_id,
                        porcoes
                    )
                    VALUES (?, ?, ?)
                """, (
                    refeicao_id,
                    receita["id"],
                    receita["porcoes"]
                ))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


def excluir_cardapio(cardapio_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT id
            FROM refeicoes_cardapio
            WHERE cardapio_id = ?
        """, (cardapio_id,))

        refeicoes = cursor.fetchall()

        for refeicao in refeicoes:

            refeicao_id = refeicao[0]

            cursor.execute("""
                DELETE FROM alimentos_cardapio
                WHERE refeicao_id = ?
            """, (refeicao_id,))

            cursor.execute("""
                DELETE FROM receitas_cardapio
                WHERE refeicao_id = ?
            """, (refeicao_id,))

        cursor.execute("""
            DELETE FROM refeicoes_cardapio
            WHERE cardapio_id = ?
        """, (cardapio_id,))

        cursor.execute("""
            DELETE FROM cardapios
            WHERE id = ?
        """, (cardapio_id,))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()