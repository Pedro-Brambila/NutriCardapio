from alimentos.alimentos import criar_tabela_alimentos, pesquisar_alimento

from cardapios.cardapios import (
    criar_tabelas_cardapios,
    salvar_cardapio,
    listar_cardapios,
    buscar_cardapio,
    atualizar_cardapio,
    excluir_cardapio
)
from receitas.receitas import (
    calcular_nutrientes,
    criar_tabelas_receitas,
    salvar_receita,
    listar_receitas,
    buscar_receita,
    atualizar_receita,
    excluir_receita
)
def mostrar_alimento(alimento):
    print("----------------------------------------")
    print(f"ID: {alimento['id']}")
    print(f"Nome: {alimento['nome']}")
    print(f"Fonte: {alimento['fonte']}")
    print(f"Calorias: {alimento['energia_kcal']:.2f} kcal")
    print(f"Proteínas: {alimento['proteina_g']:.2f} g")
    print(f"Carboidratos: {alimento['carboidrato_g']:.2f} g")
    print(f"Gorduras: {alimento['gordura_g']:.2f} g")
    print(f"Fibras: {alimento['fibra_g']:.2f} g")


def pesquisar():
    nome = input("\nDigite o nome do alimento: ").strip()

    if not nome:
        print("Digite algum alimento.")
        return

    resultados = pesquisar_alimento(nome)

    if not resultados:
        print("\nNenhum alimento encontrado.")
        return

    print("\nAlimentos encontrados:")

    for alimento in resultados:
        mostrar_alimento(alimento)


def calcular():
    nome = input("\nDigite o alimento: ").strip()

    resultados = pesquisar_alimento(nome)

    if not resultados:
        print("\nNenhum alimento encontrado.")
        return

    print("\nResultados:")

    for i, alimento in enumerate(resultados, start=1):
        print(
            f"{i} - {alimento['nome']} "
            f"({alimento['fonte']})"
        )

    try:
        escolha = int(input("\nEscolha o número do alimento: "))
        alimento = resultados[escolha - 1]

        quantidade = float(
            input("Digite a quantidade em gramas: ")
        )

    except (ValueError, IndexError):
        print("\nEscolha inválida.")
        return

    resultado = calcular_nutrientes(
        alimento["nome"],
        quantidade
    )

    print("\n==============================")
    print("       RESULTADO")
    print("==============================")

    print(f"Alimento: {alimento['nome']}")
    print(f"Quantidade: {quantidade:.2f} g")
    print()
    print(f"Calorias:      {resultado['energia_kcal']:.2f} kcal")
    print(f"Proteínas:     {resultado['proteina_g']:.2f} g")
    print(f"Carboidratos:  {resultado['carboidrato_g']:.2f} g")
    print(f"Gorduras:      {resultado['gordura_g']:.2f} g")
    print(f"Fibras:        {resultado['fibra_g']:.2f} g")

def criar_receita():
    print()
    print("==============================")
    print("        NOVA RECEITA")
    print("==============================")

    nome_receita = input("Nome da receita: ").strip()

    if not nome_receita:
        print("O nome da receita não pode ficar vazio.")
        return

    while True:
        try:
            porcoes = int(
                input("Número de porções: ")
            )

            if porcoes <= 0:
                print("Digite um número maior que zero.")
                continue

            break

        except ValueError:
            print("Digite um número válido.")

    ingredientes = []

    while True:

        print()
        print("------------------------------")
        print("ADICIONAR INGREDIENTE")
        print("------------------------------")

        nome_alimento = input(
            "Digite o alimento: "
        ).strip()

        resultados = pesquisar_alimento(nome_alimento)

        if not resultados:
            print("Nenhum alimento encontrado.")
            continue

        print()
        print("Resultados:")

        for i, alimento in enumerate(resultados, start=1):
            print(
                f"{i} - {alimento['nome']} "
                f"({alimento['fonte']})"
            )

        try:
            escolha = int(
                input("Escolha o alimento: ")
            )

            alimento = resultados[escolha - 1]

        except (ValueError, IndexError):
            print("Escolha inválida.")
            continue

        try:
            quantidade = float(
                input("Quantidade em gramas: ")
            )

            if quantidade <= 0:
                print("A quantidade deve ser maior que zero.")
                continue

        except ValueError:
            print("Digite uma quantidade válida.")
            continue

        ingredientes.append({
            "id": alimento["id"],
            "nome": alimento["nome"],
            "quantidade": quantidade
        })

        print()
        print(
            f"✓ {alimento['nome']} "
            f"({quantidade:.2f} g) adicionado!"
        )

        continuar = input(
            "Adicionar outro ingrediente? (s/n): "
        ).strip().lower()

        if continuar != "s":
            break

    if not ingredientes:
        print("Nenhum ingrediente foi adicionado.")
        return

    # Calcula os nutrientes da receita
    total = {
        "energia_kcal": 0,
        "proteina_g": 0,
        "carboidrato_g": 0,
        "gordura_g": 0,
        "fibra_g": 0
    }

    for ingrediente in ingredientes:

        resultado = calcular_nutrientes(
            ingrediente["nome"],
            ingrediente["quantidade"]
        )

        if resultado:
            total["energia_kcal"] += resultado["energia_kcal"]
            total["proteina_g"] += resultado["proteina_g"]
            total["carboidrato_g"] += resultado["carboidrato_g"]
            total["gordura_g"] += resultado["gordura_g"]
            total["fibra_g"] += resultado["fibra_g"]

    # Mostra resultado
    print()
    print("==============================")
    print("       RECEITA FINAL")
    print("==============================")

    print(f"Nome: {nome_receita}")
    print(f"Porções: {porcoes}")
    print()

    print("Ingredientes:")

    for ingrediente in ingredientes:
        print(
            f"- {ingrediente['nome']} "
            f"({ingrediente['quantidade']:.2f} g)"
        )

    print()
    print("------ TOTAL ------")

    print(
        f"Calorias:      "
        f"{total['energia_kcal']:.2f} kcal"
    )

    print(
        f"Proteínas:     "
        f"{total['proteina_g']:.2f} g"
    )

    print(
        f"Carboidratos:  "
        f"{total['carboidrato_g']:.2f} g"
    )

    print(
        f"Gorduras:      "
        f"{total['gordura_g']:.2f} g"
    )

    print(
        f"Fibras:        "
        f"{total['fibra_g']:.2f} g"
    )

    print()
    print("------ POR PORÇÃO ------")

    print(
        f"Calorias:      "
        f"{total['energia_kcal'] / porcoes:.2f} kcal"
    )

    print(
        f"Proteínas:     "
        f"{total['proteina_g'] / porcoes:.2f} g"
    )

    print(
        f"Carboidratos:  "
        f"{total['carboidrato_g'] / porcoes:.2f} g"
    )

    print(
        f"Gorduras:      "
        f"{total['gordura_g'] / porcoes:.2f} g"
    )

    print(
        f"Fibras:        "
        f"{total['fibra_g'] / porcoes:.2f} g"
    )

    # Salva a receita
    salvar_receita(
        nome_receita,
        porcoes,
        ingredientes
    )

    print()
    print("✓ Receita salva com sucesso!")
def editar_receita(receita_id):
    receita = buscar_receita(receita_id)

    if receita is None:
        print("Receita não encontrada.")
        return

    print()
    print("==============================")
    print("        EDITAR RECEITA")
    print("==============================")

    print(f"Nome atual: {receita['nome']}")

    novo_nome = input(
        "Novo nome (ENTER para manter): "
    ).strip()

    if not novo_nome:
        novo_nome = receita["nome"]

    print()
    print(f"Porções atuais: {receita['porcoes']}")

    entrada_porcoes = input(
        "Novo número de porções (ENTER para manter): "
    ).strip()

    if entrada_porcoes:
        try:
            novas_porcoes = int(entrada_porcoes)

            if novas_porcoes <= 0:
                print("O número de porções deve ser maior que zero.")
                return

        except ValueError:
            print("Número de porções inválido.")
            return
    else:
        novas_porcoes = receita["porcoes"]

    print()
    print("Agora vamos recriar os ingredientes.")
    print("Os ingredientes atuais serão substituídos.")
    print()

    ingredientes = []

    while True:

        nome_alimento = input(
            "Digite o nome do alimento "
            "(ou ENTER para terminar): "
        ).strip()

        if not nome_alimento:
            break

        resultados = pesquisar_alimento(nome_alimento)

        if not resultados:
            print("Alimento não encontrado.")
            continue

        print()

        for i, alimento in enumerate(resultados, start=1):
            print(
                f"{i} - {alimento['nome']} "
                f"[{alimento['fonte']}]"
            )

        print()

        try:
            escolha = int(
                input("Escolha o alimento: ")
            )

            if escolha < 1 or escolha > len(resultados):
                print("Escolha inválida.")
                continue

        except ValueError:
            print("Digite um número válido.")
            continue

        alimento = resultados[escolha - 1]

        try:
            quantidade = float(
                input(
                    f"Quantidade de {alimento['nome']} em gramas: "
                )
            )

            if quantidade <= 0:
                print("A quantidade deve ser maior que zero.")
                continue

        except ValueError:
            print("Quantidade inválida.")
            continue

        ingredientes.append({
            "id": alimento["id"],
            "nome": alimento["nome"],
            "quantidade": quantidade
        })

        print("✓ Ingrediente adicionado.")
        print()

    if not ingredientes:
        print("A receita precisa ter pelo menos um ingrediente.")
        return

    try:
        atualizar_receita(
            receita_id,
            novo_nome,
            novas_porcoes,
            ingredientes
        )

        print()
        print("✓ Receita atualizada com sucesso!")

    except Exception as erro:
        print()
        print("Não foi possível atualizar a receita.")
        print(f"Erro: {erro}")
def excluir_receita_menu(receita_id):
    receita = buscar_receita(receita_id)

    if receita is None:
        print("Receita não encontrada.")
        return

    print()
    print("==============================")
    print("       EXCLUIR RECEITA")
    print("==============================")

    print(f"Receita: {receita['nome']}")

    confirmacao = input(
        "Tem certeza que deseja excluir? (s/n): "
    ).strip().lower()

    if confirmacao != "s":
        print("Exclusão cancelada.")
        return

    try:
        excluir_receita(receita_id)

        print()
        print("✓ Receita excluída com sucesso!")

    except Exception as erro:
        print()
        print("Não foi possível excluir a receita.")
        print(f"Erro: {erro}")
        
def minhas_receitas():
    while True:

        receitas = listar_receitas()

        print()
        print("==============================")
        print("       MINHAS RECEITAS")
        print("==============================")

        if not receitas:
            print("Nenhuma receita cadastrada.")
            return

        for i, receita in enumerate(receitas, start=1):
            print(
                f"{i} - {receita[1]} "
                f"({receita[2]} porções)"
            )

        print()
        print("0 - Voltar")

        try:
            escolha = int(
                input("Escolha uma receita: ")
            )
        except ValueError:
            print("Escolha inválida.")
            continue

        if escolha == 0:
            return

        if escolha < 1 or escolha > len(receitas):
            print("Escolha inválida.")
            continue

        receita_id = receitas[escolha - 1][0]

        while True:

            receita = buscar_receita(receita_id)

            if receita is None:
                break

            print()
            print("==============================")
            print(f"       {receita['nome']}")
            print("==============================")
            print("1 - Visualizar")
            print("2 - Editar")
            print("3 - Excluir")
            print("0 - Voltar")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":

                visualizar_receita(receita_id)

            elif opcao == "2":

                editar_receita(receita_id)

            elif opcao == "3":

                excluir_receita_menu(receita_id)
                break

            elif opcao == "0":

                break

            else:

                print("Opção inválida.")
def visualizar_receita(receita_id):
    receita = buscar_receita(receita_id)

    if receita is None:
        print("Receita não encontrada.")
        return

    print()
    print("==============================")
    print("       RECEITA")
    print("==============================")

    print(f"Nome: {receita['nome']}")
    print(f"Porções: {receita['porcoes']}")

    print()
    print("INGREDIENTES")
    print("------------------------------")

    for ingrediente in receita["ingredientes"]:

        print(
            f"- {ingrediente['nome']} "
            f"— {ingrediente['quantidade']:.2f} g"
        )

    total = receita["total"]
    porcoes = receita["porcoes"]

    print()
    print("NUTRIENTES DA RECEITA")
    print("------------------------------")

    print(
        f"Calorias:      "
        f"{total['energia_kcal']:.2f} kcal"
    )

    print(
        f"Proteínas:     "
        f"{total['proteina_g']:.2f} g"
    )

    print(
        f"Carboidratos:  "
        f"{total['carboidrato_g']:.2f} g"
    )

    print(
        f"Gorduras:      "
        f"{total['gordura_g']:.2f} g"
    )

    print(
        f"Fibras:        "
        f"{total['fibra_g']:.2f} g"
    )

    print()
    print("NUTRIENTES POR PORÇÃO")
    print("------------------------------")

    print(
        f"Calorias:      "
        f"{total['energia_kcal'] / porcoes:.2f} kcal"
    )

    print(
        f"Proteínas:     "
        f"{total['proteina_g'] / porcoes:.2f} g"
    )

    print(
        f"Carboidratos:  "
        f"{total['carboidrato_g'] / porcoes:.2f} g"
    )

    print(
        f"Gorduras:      "
        f"{total['gordura_g'] / porcoes:.2f} g"
    )

    print(
        f"Fibras:        "
        f"{total['fibra_g'] / porcoes:.2f} g"
    )

    print()
    input("Pressione ENTER para voltar...")      

def criar_cardapio():
    print()
    print("==============================")
    print("        CRIAR CARDÁPIO")
    print("==============================")

    nome = input("Nome do cardápio: ").strip()

    if not nome:
        print("O nome do cardápio não pode ficar vazio.")
        return

    refeicoes = []

    print()
    print("Agora vamos adicionar as refeições.")
    print("Exemplo: Café da manhã, Almoço, Lanche, Jantar.")
    print()

    while True:

        nome_refeicao = input(
            "Nome da refeição "
            "(ou ENTER para terminar): "
        ).strip()

        if not nome_refeicao:
            break

        refeicao = {
            "nome": nome_refeicao,
            "alimentos": [],
            "receitas": []
        }

        print()
        print(f"=== {nome_refeicao} ===")
        print("1 - Adicionar alimento")
        print("2 - Adicionar receita")
        print("0 - Finalizar refeição")

        while True:

            opcao = input("Escolha: ").strip()

            if opcao == "0":
                break

            elif opcao == "1":

                nome_alimento = input(
                    "Digite o nome do alimento: "
                ).strip()

                if not nome_alimento:
                    print("Digite um alimento.")
                    continue

                resultados = pesquisar_alimento(nome_alimento)

                if not resultados:
                    print("Alimento não encontrado.")
                    continue

                print()

                for i, alimento in enumerate(resultados, start=1):
                    print(
                        f"{i} - {alimento['nome']} "
                        f"[{alimento['fonte']}]"
                    )

                print()

                try:
                    escolha = int(
                        input("Escolha o alimento: ")
                    )

                    if escolha < 1 or escolha > len(resultados):
                        print("Escolha inválida.")
                        continue

                except ValueError:
                    print("Digite um número válido.")
                    continue

                alimento = resultados[escolha - 1]

                try:
                    quantidade = float(
                        input(
                            f"Quantidade de "
                            f"{alimento['nome']} em gramas: "
                        )
                    )

                    if quantidade <= 0:
                        print(
                            "A quantidade deve ser maior que zero."
                        )
                        continue

                except ValueError:
                    print("Quantidade inválida.")
                    continue

                refeicao["alimentos"].append({
                    "id": alimento["id"],
                    "nome": alimento["nome"],
                    "quantidade": quantidade
                })

                print("✓ Alimento adicionado.")

            elif opcao == "2":

                receitas = listar_receitas()

                if not receitas:
                    print("Nenhuma receita cadastrada.")
                    continue

                print()
                print("RECEITAS DISPONÍVEIS")

                for i, receita in enumerate(receitas, start=1):
                    print(
                        f"{i} - {receita[1]} "
                        f"({receita[2]} porções)"
                    )

                print()

                try:
                    escolha = int(
                        input("Escolha a receita: ")
                    )

                    if escolha < 1 or escolha > len(receitas):
                        print("Escolha inválida.")
                        continue

                except ValueError:
                    print("Digite um número válido.")
                    continue

                receita = receitas[escolha - 1]

                try:
                    porcoes = float(
                        input(
                            "Quantidade de porções da receita: "
                        )
                    )

                    if porcoes <= 0:
                        print(
                            "A quantidade deve ser maior que zero."
                        )
                        continue

                except ValueError:
                    print("Quantidade inválida.")
                    continue

                refeicao["receitas"].append({
                    "id": receita[0],
                    "nome": receita[1],
                    "porcoes": porcoes
                })

                print("✓ Receita adicionada.")

            else:
                print("Opção inválida.")

        if not refeicao["alimentos"] and not refeicao["receitas"]:
            print(
                "A refeição não possui nenhum item "
                "e não será adicionada."
            )
            continue

        refeicoes.append(refeicao)

        print()
        print(
            f"✓ Refeição '{nome_refeicao}' adicionada ao cardápio."
        )

    if not refeicoes:
        print()
        print("O cardápio precisa ter pelo menos uma refeição.")
        return

    try:
        cardapio_id = salvar_cardapio(
            nome,
            refeicoes
        )

        print()
        print("==============================")
        print("✓ CARDÁPIO SALVO COM SUCESSO!")
        print("==============================")
        print(f"ID: {cardapio_id}")
        print(f"Nome: {nome}")
        print(f"Refeições: {len(refeicoes)}")

    except Exception as erro:
        print()
        print("Não foi possível salvar o cardápio.")
        print(f"Erro: {erro}")

def editar_cardapio(cardapio_id):
    cardapio = buscar_cardapio(cardapio_id)

    if cardapio is None:
        print("Cardápio não encontrado.")
        return

    print()
    print("==============================")
    print("        EDITAR CARDÁPIO")
    print("==============================")

    print(f"Nome atual: {cardapio['nome']}")

    novo_nome = input(
        "Novo nome (ENTER para manter): "
    ).strip()

    if not novo_nome:
        novo_nome = cardapio["nome"]

    refeicoes = []

    print()
    print("Vamos recriar as refeições do cardápio.")
    print("Você poderá manter, remover ou modificar")
    print("as refeições existentes.")
    print()

    while True:

        nome_refeicao = input(
            "Nome da refeição "
            "(ou ENTER para terminar): "
        ).strip()

        if not nome_refeicao:
            break

        refeicao = {
            "nome": nome_refeicao,
            "alimentos": [],
            "receitas": []
        }

        print()
        print(f"=== {nome_refeicao} ===")
        print("1 - Adicionar alimento")
        print("2 - Adicionar receita")
        print("0 - Finalizar refeição")

        while True:

            opcao = input("Escolha: ").strip()

            if opcao == "0":
                break

            elif opcao == "1":

                nome_alimento = input(
                    "Digite o nome do alimento: "
                ).strip()

                if not nome_alimento:
                    print("Digite um alimento.")
                    continue

                resultados = pesquisar_alimento(nome_alimento)

                if not resultados:
                    print("Alimento não encontrado.")
                    continue

                print()

                for i, alimento in enumerate(resultados, start=1):
                    print(
                        f"{i} - {alimento['nome']} "
                        f"[{alimento['fonte']}]"
                    )

                print()

                try:
                    escolha = int(
                        input("Escolha o alimento: ")
                    )

                    if escolha < 1 or escolha > len(resultados):
                        print("Escolha inválida.")
                        continue

                except ValueError:
                    print("Digite um número válido.")
                    continue

                alimento = resultados[escolha - 1]

                try:
                    quantidade = float(
                        input(
                            f"Quantidade de "
                            f"{alimento['nome']} em gramas: "
                        )
                    )

                    if quantidade <= 0:
                        print(
                            "A quantidade deve ser maior que zero."
                        )
                        continue

                except ValueError:
                    print("Quantidade inválida.")
                    continue

                refeicao["alimentos"].append({
                    "id": alimento["id"],
                    "nome": alimento["nome"],
                    "quantidade": quantidade
                })

                print("✓ Alimento adicionado.")

            elif opcao == "2":

                receitas = listar_receitas()

                if not receitas:
                    print("Nenhuma receita cadastrada.")
                    continue

                print()
                print("RECEITAS DISPONÍVEIS")

                for i, receita in enumerate(receitas, start=1):
                    print(
                        f"{i} - {receita[1]} "
                        f"({receita[2]} porções)"
                    )

                print()

                try:
                    escolha = int(
                        input("Escolha a receita: ")
                    )

                    if escolha < 1 or escolha > len(receitas):
                        print("Escolha inválida.")
                        continue

                except ValueError:
                    print("Digite um número válido.")
                    continue

                receita = receitas[escolha - 1]

                try:
                    porcoes = float(
                        input(
                            "Quantidade de porções da receita: "
                        )
                    )

                    if porcoes <= 0:
                        print(
                            "A quantidade deve ser maior que zero."
                        )
                        continue

                except ValueError:
                    print("Quantidade inválida.")
                    continue

                refeicao["receitas"].append({
                    "id": receita[0],
                    "nome": receita[1],
                    "porcoes": porcoes
                })

                print("✓ Receita adicionada.")

            else:
                print("Opção inválida.")

        if not refeicao["alimentos"] and not refeicao["receitas"]:
            print(
                "A refeição não possui itens "
                "e não será adicionada."
            )
            continue

        refeicoes.append(refeicao)

        print()
        print(
            f"✓ Refeição '{nome_refeicao}' adicionada."
        )

    if not refeicoes:
        print()
        print(
            "O cardápio precisa ter pelo menos "
            "uma refeição."
        )
        return

    try:

        atualizar_cardapio(
            cardapio_id,
            novo_nome,
            refeicoes
        )

        print()
        print("✓ Cardápio atualizado com sucesso!")

    except Exception as erro:

        print()
        print("Não foi possível atualizar o cardápio.")
        print(f"Erro: {erro}")

def excluir_cardapio_menu(cardapio_id):
    cardapio = buscar_cardapio(cardapio_id)

    if cardapio is None:
        print("Cardápio não encontrado.")
        return

    print()
    print("==============================")
    print("       EXCLUIR CARDÁPIO")
    print("==============================")

    print(f"Cardápio: {cardapio['nome']}")

    confirmacao = input(
        "Tem certeza que deseja excluir? (s/n): "
    ).strip().lower()

    if confirmacao != "s":
        print("Exclusão cancelada.")
        return

    try:

        excluir_cardapio(cardapio_id)

        print()
        print("✓ Cardápio excluído com sucesso!")

    except Exception as erro:

        print()
        print("Não foi possível excluir o cardápio.")
        print(f"Erro: {erro}")

def meus_cardapios():
    while True:

        cardapios = listar_cardapios()

        print()
        print("==============================")
        print("        MEUS CARDÁPIOS")
        print("==============================")

        if not cardapios:
            print("Nenhum cardápio cadastrado.")
            return

        for i, cardapio in enumerate(cardapios, start=1):
            print(
                f"{i} - {cardapio[1]}"
            )

        print()
        print("0 - Voltar")

        escolha = input(
            "Escolha um cardápio: "
        ).strip()

        if escolha == "0":
            return

        try:

            escolha = int(escolha)

            if escolha < 1 or escolha > len(cardapios):
                print("Escolha inválida.")
                continue

        except ValueError:

            print("Escolha inválida.")
            continue

        cardapio_id = cardapios[escolha - 1][0]

        while True:

            cardapio = buscar_cardapio(cardapio_id)

            if cardapio is None:
                break

            print()
            print("==============================")
            print(f"      {cardapio['nome']}")
            print("==============================")

            print("1 - Visualizar")
            print("2 - Editar")
            print("3 - Excluir")
            print("0 - Voltar")

            opcao = input(
                "Escolha uma opção: "
            ).strip()

            if opcao == "1":

                print()
                print("VISUALIZAÇÃO COMPLETA DO CARDÁPIO")
                print("--------------------------------")

                for refeicao in cardapio["refeicoes"]:

                    print()
                    print(
                        f"### {refeicao['nome']} ###"
                    )

                    for alimento in refeicao["alimentos"]:

                        print(
                            f"- {alimento['nome']} "
                            f"({alimento['fonte']}) "
                            f"— {alimento['quantidade']:.2f} g"
                        )

                    for receita in refeicao["receitas"]:

                        print(
                            f"- Receita: {receita['nome']} "
                            f"— {receita['porcoes']:.2f} porção(ões)"
                        )

                print()
                input(
                    "Pressione ENTER para voltar..."
                )

            elif opcao == "2":

                editar_cardapio(cardapio_id)

            elif opcao == "3":

                excluir_cardapio_menu(cardapio_id)

                break

            elif opcao == "0":

                break

            else:

                print("Opção inválida.")

def menu():
    while True:

        print()
        print("==============================")
        print("       NUTRICARDÁPIO")
        print("==============================")
        print("1 - Pesquisar alimento")
        print("2 - Calcular quantidade")
        print("3 - Criar receita")
        print("4 - Minhas receitas")
        print("5 - Criar cardápio")
        print("6 - Meus cardápios")
        print("0 - Sair")
        print("==============================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            pesquisar()

        elif opcao == "2":
            calcular()

        elif opcao == "3":
            criar_receita()

        elif opcao == "4":

            minhas_receitas()
        elif opcao == "5":
             criar_cardapio()

        elif opcao == "6":
            meus_cardapios()

        elif opcao == "0":
            print("\nAté mais!")
            break

        else:
            print("\nOpção inválida.")


if __name__ == "__main__":
    criar_tabela_alimentos()
    criar_tabelas_receitas()
    criar_tabelas_cardapios()
    menu()