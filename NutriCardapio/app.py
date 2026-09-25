import streamlit as st
import pandas as pd

from alimentos.alimentos import criar_tabela_alimentos, pesquisar_alimento
from cardapios.cardapios import (
    criar_tabelas_cardapios,
    salvar_cardapio,
    listar_cardapios,
    buscar_cardapio,
    atualizar_cardapio,
    excluir_cardapio,
)
from receitas.receitas import (
    calcular_nutrientes,
    criar_tabelas_receitas,
    salvar_receita,
    listar_receitas,
    buscar_receita,
    atualizar_receita,
    excluir_receita,
)

st.set_page_config(page_title="NutriCardápio", page_icon="🥗", layout="wide")

criar_tabela_alimentos()
criar_tabelas_receitas()
criar_tabelas_cardapios()

MACROS = [
    ("energia_kcal", "Calorias", "kcal"),
    ("proteina_g", "Proteínas", "g"),
    ("carboidrato_g", "Carboidratos", "g"),
    ("gordura_g", "Gorduras", "g"),
    ("fibra_g", "Fibras", "g"),
]

TOTAL_ZERO = {"energia_kcal": 0, "proteina_g": 0, "carboidrato_g": 0, "gordura_g": 0, "fibra_g": 0}


# ---------------------------------------------------------------------------
# Funções auxiliares (usadas por várias páginas)
# ---------------------------------------------------------------------------

def show_macro_metrics(dados):
    cols = st.columns(len(MACROS))
    for col, (chave, rotulo, unidade) in zip(cols, MACROS):
        valor = dados.get(chave, 0) or 0
        col.metric(rotulo, f"{valor:.1f} {unidade}")


def calcular_totais(ingredientes):
    total = dict(TOTAL_ZERO)
    for ing in ingredientes:
        resultado = calcular_nutrientes(ing["nome"], ing["quantidade"])
        if resultado:
            for chave in total:
                total[chave] += resultado[chave]
    return total


def render_ingredientes_builder(state_key):
    """Cria a UI de adicionar/remover ingredientes e devolve a lista atual."""
    if state_key not in st.session_state:
        st.session_state[state_key] = []

    busca_col, qtd_col, btn_col = st.columns([3, 1, 1])

    with busca_col:
        nome_busca = st.text_input(
            "Buscar alimento", key=f"{state_key}_busca", placeholder="Digite o nome do alimento..."
        )

    alimento_escolhido = None
    if nome_busca:
        resultados = pesquisar_alimento(nome_busca)
        if resultados:
            opcoes = {f"{a['nome']} ({a['fonte']})": a for a in resultados}
            escolha = st.selectbox("Selecione o alimento", list(opcoes.keys()), key=f"{state_key}_select")
            alimento_escolhido = opcoes[escolha]
        else:
            st.caption("Nenhum alimento encontrado.")

    with qtd_col:
        quantidade = st.number_input(
            "Gramas", min_value=0.0, value=100.0, step=10.0, key=f"{state_key}_qtd"
        )

    with btn_col:
        st.write("")
        st.write("")
        if st.button("➕ Adicionar", key=f"{state_key}_add"):
            if alimento_escolhido and quantidade > 0:
                st.session_state[state_key].append(
                    {
                        "id": alimento_escolhido["id"],
                        "nome": alimento_escolhido["nome"],
                        "quantidade": quantidade,
                    }
                )
                st.rerun()
            else:
                st.warning("Escolha um alimento e uma quantidade válida.")

    ingredientes = st.session_state[state_key]

    if ingredientes:
        for i, ing in enumerate(ingredientes):
            c1, c2, c3 = st.columns([4, 2, 1])
            c1.write(ing["nome"])
            c2.write(f"{ing['quantidade']:.0f} g")
            if c3.button("🗑️", key=f"{state_key}_rm_{i}"):
                ingredientes.pop(i)
                st.rerun()
    else:
        st.caption("Nenhum ingrediente adicionado ainda.")

    return ingredientes


def render_refeicao_builder(refeicao, key_prefix, receitas_disponiveis):
    """Permite adicionar alimentos e receitas dentro de uma refeição (dict mutado in place)."""
    tab_alim, tab_rec = st.tabs(["🥗 Alimentos", "🍳 Receitas prontas"])

    with tab_alim:
        nome_busca = st.text_input("Buscar alimento", key=f"{key_prefix}_busca_alim")
        alimento_escolhido = None
        if nome_busca:
            resultados = pesquisar_alimento(nome_busca)
            if resultados:
                opcoes = {f"{a['nome']} ({a['fonte']})": a for a in resultados}
                escolha = st.selectbox("Selecione", list(opcoes.keys()), key=f"{key_prefix}_select_alim")
                alimento_escolhido = opcoes[escolha]
            else:
                st.caption("Nenhum alimento encontrado.")

        c1, c2 = st.columns([2, 1])
        quantidade = c1.number_input(
            "Gramas", min_value=0.0, value=100.0, step=10.0, key=f"{key_prefix}_qtd_alim"
        )
        with c2:
            st.write("")
            st.write("")
            if st.button("➕ Adicionar", key=f"{key_prefix}_add_alim"):
                if alimento_escolhido and quantidade > 0:
                    refeicao["alimentos"].append(
                        {
                            "id": alimento_escolhido["id"],
                            "nome": alimento_escolhido["nome"],
                            "quantidade": quantidade,
                        }
                    )
                    st.rerun()
                else:
                    st.warning("Escolha um alimento e quantidade válida.")

        for i, alim in enumerate(refeicao["alimentos"]):
            cc1, cc2, cc3 = st.columns([4, 2, 1])
            cc1.write(alim["nome"])
            cc2.write(f"{alim['quantidade']:.0f} g")
            if cc3.button("🗑️", key=f"{key_prefix}_rm_alim_{i}"):
                refeicao["alimentos"].pop(i)
                st.rerun()

    with tab_rec:
        if receitas_disponiveis:
            opcoes_rec = {f"{r[1]} ({r[2]} porções)": r for r in receitas_disponiveis}
            escolha_rec = st.selectbox("Receita", list(opcoes_rec.keys()), key=f"{key_prefix}_select_rec")
            porcoes_rec = st.number_input(
                "Quantas porções usar", min_value=0.5, value=1.0, step=0.5, key=f"{key_prefix}_porcoes_rec"
            )
            if st.button("➕ Adicionar Receita", key=f"{key_prefix}_add_rec"):
                r = opcoes_rec[escolha_rec]
                refeicao["receitas"].append({"id": r[0], "nome": r[1], "porcoes": porcoes_rec})
                st.rerun()
        else:
            st.caption("Nenhuma receita cadastrada ainda.")

        for i, rec in enumerate(refeicao["receitas"]):
            cc1, cc2, cc3 = st.columns([4, 2, 1])
            cc1.write(rec["nome"])
            cc2.write(f"{rec['porcoes']:.1f} porção(ões)")
            if cc3.button("🗑️", key=f"{key_prefix}_rm_rec_{i}"):
                refeicao["receitas"].pop(i)
                st.rerun()


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------

def pagina_inicio():
    st.title("🥗 NutriCardápio")
    st.caption("Monte receitas e cardápios com base nos dados nutricionais da tabela TACO.")

    total_alimentos = len(pesquisar_alimento(""))
    total_receitas = len(listar_receitas())
    total_cardapios = len(listar_cardapios())

    col1, col2, col3 = st.columns(3)
    col1.metric("🍎 Alimentos disponíveis", total_alimentos)
    col2.metric("🍳 Receitas cadastradas", total_receitas)
    col3.metric("📋 Cardápios criados", total_cardapios)

    st.markdown("---")
    st.markdown(
        """
        ### Como usar
        - **🔍 Alimentos** — pesquise qualquer alimento e calcule sua informação nutricional.
        - **🍳 Receitas** — monte receitas somando ingredientes e veja o total nutricional por porção.
        - **📋 Cardápios** — organize receitas e alimentos em refeições e cardápios completos.
        """
    )


def pagina_alimentos():
    st.subheader("🔍 Pesquisar Alimentos")
    nome = st.text_input("Digite o nome do alimento", placeholder="Ex: arroz, frango, banana...")

    if not nome:
        st.info("Digite o nome de um alimento para começar a busca.")
        return

    resultados = pesquisar_alimento(nome)
    if not resultados:
        st.warning("Nenhum alimento encontrado.")
        return

    df = pd.DataFrame(resultados)[
        ["nome", "fonte", "energia_kcal", "proteina_g", "carboidrato_g", "gordura_g", "fibra_g"]
    ]
    df.columns = ["Alimento", "Fonte", "Calorias (kcal)", "Proteínas (g)", "Carboidratos (g)", "Gorduras (g)", "Fibras (g)"]
    st.dataframe(df, width="stretch", hide_index=True)

    st.markdown("---")
    st.markdown("### 🧮 Calcular quantidade específica")

    opcoes = {f"{a['nome']} ({a['fonte']})": a for a in resultados}
    escolha = st.selectbox("Escolha o alimento", list(opcoes.keys()))
    quantidade = st.number_input("Quantidade em gramas", min_value=0.0, value=100.0, step=10.0)

    if quantidade > 0:
        alimento = opcoes[escolha]
        resultado = calcular_nutrientes(alimento["nome"], quantidade)
        if resultado:
            show_macro_metrics(resultado)


def pagina_nova_receita():
    st.markdown("### ➕ Nova Receita")

    if "nr_versao" not in st.session_state:
        st.session_state["nr_versao"] = 0
    versao = st.session_state["nr_versao"]

    nome_receita = st.text_input("Nome da receita", key=f"nr_nome_{versao}")
    porcoes = st.number_input("Número de porções", min_value=1, value=1, step=1, key=f"nr_porcoes_{versao}")

    ingredientes = render_ingredientes_builder(f"nr_ingredientes_{versao}")

    if ingredientes:
        total = calcular_totais(ingredientes)
        st.markdown("---")
        st.markdown("**Total da receita**")
        show_macro_metrics(total)
        st.markdown("**Por porção**")
        por_porcao = {k: v / porcoes for k, v in total.items()}
        show_macro_metrics(por_porcao)

    st.markdown("---")
    if st.button("💾 Salvar Receita", type="primary"):
        if not nome_receita.strip():
            st.error("Digite um nome para a receita.")
        elif not ingredientes:
            st.error("Adicione pelo menos um ingrediente.")
        else:
            try:
                salvar_receita(nome_receita.strip(), porcoes, ingredientes)
                st.toast(f"Receita '{nome_receita}' salva com sucesso!", icon="✅")
                st.session_state["nr_versao"] += 1
                st.rerun()
            except Exception as erro:
                st.error(f"Não foi possível salvar (nome já existe?). Detalhe: {erro}")


def pagina_minhas_receitas():
    st.markdown("### 📖 Minhas Receitas")
    receitas = listar_receitas()

    if not receitas:
        st.info("Nenhuma receita cadastrada ainda.")
        return

    for receita_id, nome, porcoes in receitas:
        with st.expander(f"🍳 {nome} — {porcoes} porção(ões)"):
            editando_key = f"editando_receita_{receita_id}"

            if st.session_state.get(editando_key, False):
                novo_nome = st.text_input("Nome", value=nome, key=f"edit_nome_{receita_id}")
                novas_porcoes = st.number_input(
                    "Porções", min_value=1, value=int(porcoes), key=f"edit_porcoes_{receita_id}"
                )

                ing_state_key = f"edit_ing_{receita_id}"
                if ing_state_key not in st.session_state:
                    detalhe = buscar_receita(receita_id)
                    st.session_state[ing_state_key] = [
                        {"id": ing["id"], "nome": ing["nome"], "quantidade": ing["quantidade"]}
                        for ing in detalhe["ingredientes"]
                    ]

                ingredientes = render_ingredientes_builder(ing_state_key)

                col1, col2 = st.columns(2)
                if col1.button("💾 Salvar alterações", key=f"save_{receita_id}"):
                    if not novo_nome.strip():
                        st.error("Nome não pode ficar vazio.")
                    elif not ingredientes:
                        st.error("Adicione pelo menos um ingrediente.")
                    else:
                        try:
                            atualizar_receita(receita_id, novo_nome.strip(), novas_porcoes, ingredientes)
                            st.toast("Receita atualizada!", icon="✅")
                            st.session_state[editando_key] = False
                            del st.session_state[ing_state_key]
                            st.rerun()
                        except Exception as erro:
                            st.error(f"Erro: {erro}")
                if col2.button("Cancelar", key=f"cancel_{receita_id}"):
                    st.session_state[editando_key] = False
                    st.session_state.pop(ing_state_key, None)
                    st.rerun()
            else:
                detalhe = buscar_receita(receita_id)
                st.markdown("**Ingredientes:**")
                for ing in detalhe["ingredientes"]:
                    st.write(f"- {ing['nome']} ({ing['quantidade']:.0f} g)")

                st.markdown("**Total:**")
                show_macro_metrics(detalhe["total"])
                st.markdown("**Por porção:**")
                por_porcao = {k: v / porcoes for k, v in detalhe["total"].items()}
                show_macro_metrics(por_porcao)

                col1, col2 = st.columns(2)
                if col1.button("✏️ Editar", key=f"editbtn_{receita_id}"):
                    st.session_state[editando_key] = True
                    st.rerun()
                if col2.button("🗑️ Excluir", key=f"delbtn_{receita_id}"):
                    st.session_state[f"confirm_del_receita_{receita_id}"] = True
                    st.rerun()

                if st.session_state.get(f"confirm_del_receita_{receita_id}", False):
                    st.warning(f"Tem certeza que deseja excluir '{nome}'?")
                    c1, c2 = st.columns(2)
                    if c1.button("Sim, excluir", key=f"confirm_yes_{receita_id}"):
                        excluir_receita(receita_id)
                        st.toast("Receita excluída.", icon="🗑️")
                        st.session_state[f"confirm_del_receita_{receita_id}"] = False
                        st.rerun()
                    if c2.button("Cancelar", key=f"confirm_no_{receita_id}"):
                        st.session_state[f"confirm_del_receita_{receita_id}"] = False
                        st.rerun()


def pagina_novo_cardapio():
    st.markdown("### ➕ Novo Cardápio")

    if "ncd_versao" not in st.session_state:
        st.session_state["ncd_versao"] = 0
    versao = st.session_state["ncd_versao"]

    nome_cardapio = st.text_input("Nome do cardápio", key=f"ncd_nome_{versao}")

    refeicoes_key = f"ncd_refeicoes_{versao}"
    if refeicoes_key not in st.session_state:
        st.session_state[refeicoes_key] = []

    st.markdown("#### Refeições")
    col1, col2 = st.columns([4, 1])
    nova_refeicao_nome = col1.text_input(
        "Nome da refeição (ex: Café da manhã)", key=f"ncd_nova_refeicao_{versao}", label_visibility="collapsed",
        placeholder="Nome da refeição (ex: Café da manhã)"
    )
    with col2:
        if st.button("➕ Adicionar Refeição", key=f"ncd_add_refeicao_{versao}"):
            if nova_refeicao_nome.strip():
                st.session_state[refeicoes_key].append(
                    {"nome": nova_refeicao_nome.strip(), "alimentos": [], "receitas": []}
                )
                st.rerun()
            else:
                st.warning("Digite um nome para a refeição.")

    receitas_disponiveis = listar_receitas()

    for idx, refeicao in enumerate(st.session_state[refeicoes_key]):
        with st.expander(f"🍽️ {refeicao['nome']}", expanded=True):
            render_refeicao_builder(refeicao, f"ncd_{versao}_{idx}", receitas_disponiveis)
            if st.button("🗑️ Remover Refeição", key=f"ncd_rm_ref_{versao}_{idx}"):
                st.session_state[refeicoes_key].pop(idx)
                st.rerun()

    st.markdown("---")
    if st.button("💾 Salvar Cardápio", type="primary"):
        refeicoes = st.session_state[refeicoes_key]
        if not nome_cardapio.strip():
            st.error("Digite um nome para o cardápio.")
        elif not refeicoes or all(not r["alimentos"] and not r["receitas"] for r in refeicoes):
            st.error("Adicione ao menos uma refeição com itens.")
        else:
            try:
                salvar_cardapio(nome_cardapio.strip(), refeicoes)
                st.toast(f"Cardápio '{nome_cardapio}' salvo com sucesso!", icon="✅")
                st.session_state["ncd_versao"] += 1
                st.rerun()
            except Exception as erro:
                st.error(f"Não foi possível salvar (nome já existe?). Detalhe: {erro}")


def pagina_meus_cardapios():
    st.markdown("### 📖 Meus Cardápios")
    cardapios = listar_cardapios()

    if not cardapios:
        st.info("Nenhum cardápio cadastrado ainda.")
        return

    receitas_disponiveis = listar_receitas()

    for cardapio_id, nome in cardapios:
        with st.expander(f"📋 {nome}"):
            editando_key = f"editando_cardapio_{cardapio_id}"

            if st.session_state.get(editando_key, False):
                novo_nome = st.text_input("Nome do cardápio", value=nome, key=f"edit_cd_nome_{cardapio_id}")

                ref_state_key = f"edit_cd_refeicoes_{cardapio_id}"
                if ref_state_key not in st.session_state:
                    detalhe = buscar_cardapio(cardapio_id)
                    st.session_state[ref_state_key] = [
                        {
                            "nome": r["nome"],
                            "alimentos": [
                                {"id": a["id"], "nome": a["nome"], "quantidade": a["quantidade"]}
                                for a in r["alimentos"]
                            ],
                            "receitas": [
                                {"id": rc["id"], "nome": rc["nome"], "porcoes": rc["porcoes"]}
                                for rc in r["receitas"]
                            ],
                        }
                        for r in detalhe["refeicoes"]
                    ]

                col_a, col_b = st.columns([4, 1])
                nova_ref_nome = col_a.text_input(
                    "Nova refeição", key=f"edit_cd_novarefeicao_{cardapio_id}", label_visibility="collapsed",
                    placeholder="Nome da nova refeição"
                )
                with col_b:
                    if st.button("➕ Adicionar", key=f"edit_cd_addref_{cardapio_id}"):
                        if nova_ref_nome.strip():
                            st.session_state[ref_state_key].append(
                                {"nome": nova_ref_nome.strip(), "alimentos": [], "receitas": []}
                            )
                            st.rerun()

                for idx, refeicao in enumerate(st.session_state[ref_state_key]):
                    st.markdown(f"**{refeicao['nome']}**")
                    render_refeicao_builder(refeicao, f"editcd_{cardapio_id}_{idx}", receitas_disponiveis)
                    if st.button("🗑️ Remover Refeição", key=f"edit_cd_rmref_{cardapio_id}_{idx}"):
                        st.session_state[ref_state_key].pop(idx)
                        st.rerun()

                col1, col2 = st.columns(2)
                if col1.button("💾 Salvar alterações", key=f"save_cd_{cardapio_id}"):
                    refeicoes = st.session_state[ref_state_key]
                    if not novo_nome.strip():
                        st.error("Nome não pode ficar vazio.")
                    elif not refeicoes or all(not r["alimentos"] and not r["receitas"] for r in refeicoes):
                        st.error("O cardápio precisa de ao menos uma refeição com itens.")
                    else:
                        try:
                            atualizar_cardapio(cardapio_id, novo_nome.strip(), refeicoes)
                            st.toast("Cardápio atualizado!", icon="✅")
                            st.session_state[editando_key] = False
                            del st.session_state[ref_state_key]
                            st.rerun()
                        except Exception as erro:
                            st.error(f"Erro: {erro}")
                if col2.button("Cancelar", key=f"cancel_cd_{cardapio_id}"):
                    st.session_state[editando_key] = False
                    st.session_state.pop(ref_state_key, None)
                    st.rerun()
            else:
                detalhe = buscar_cardapio(cardapio_id)
                total_geral = dict(TOTAL_ZERO)

                for refeicao in detalhe["refeicoes"]:
                    st.markdown(f"**{refeicao['nome']}**")
                    for alim in refeicao["alimentos"]:
                        st.write(f"- {alim['nome']} — {alim['quantidade']:.0f} g")
                        r = calcular_nutrientes(alim["nome"], alim["quantidade"])
                        if r:
                            for k in total_geral:
                                total_geral[k] += r[k]
                    for rec in refeicao["receitas"]:
                        st.write(f"- Receita: {rec['nome']} — {rec['porcoes']:.1f} porção(ões)")
                        rd = buscar_receita(rec["id"])
                        if rd and rd["porcoes"]:
                            fator = rec["porcoes"]
                            por_porcao = {k: v / rd["porcoes"] for k, v in rd["total"].items()}
                            for k in total_geral:
                                total_geral[k] += por_porcao[k] * fator

                st.markdown("---")
                st.markdown("**Total do cardápio (todas as refeições):**")
                show_macro_metrics(total_geral)

                col1, col2 = st.columns(2)
                if col1.button("✏️ Editar", key=f"editbtn_cd_{cardapio_id}"):
                    st.session_state[editando_key] = True
                    st.rerun()
                if col2.button("🗑️ Excluir", key=f"delbtn_cd_{cardapio_id}"):
                    st.session_state[f"confirm_del_cd_{cardapio_id}"] = True
                    st.rerun()

                if st.session_state.get(f"confirm_del_cd_{cardapio_id}", False):
                    st.warning(f"Tem certeza que deseja excluir '{nome}'?")
                    c1, c2 = st.columns(2)
                    if c1.button("Sim, excluir", key=f"confirm_yes_cd_{cardapio_id}"):
                        excluir_cardapio(cardapio_id)
                        st.toast("Cardápio excluído.", icon="🗑️")
                        st.session_state[f"confirm_del_cd_{cardapio_id}"] = False
                        st.rerun()
                    if c2.button("Cancelar", key=f"confirm_no_cd_{cardapio_id}"):
                        st.session_state[f"confirm_del_cd_{cardapio_id}"] = False
                        st.rerun()


# ---------------------------------------------------------------------------
# Navegação principal
# ---------------------------------------------------------------------------

st.sidebar.title("🥗 NutriCardápio")
pagina = st.sidebar.radio(
    "Navegação",
    ["🏠 Início", "🔍 Alimentos", "🍳 Receitas", "📋 Cardápios"],
    label_visibility="collapsed",
)

if pagina == "🏠 Início":
    pagina_inicio()
elif pagina == "🔍 Alimentos":
    pagina_alimentos()
elif pagina == "🍳 Receitas":
    st.title("🍳 Receitas")
    tab1, tab2 = st.tabs(["➕ Nova Receita", "📖 Minhas Receitas"])
    with tab1:
        pagina_nova_receita()
    with tab2:
        pagina_minhas_receitas()
elif pagina == "📋 Cardápios":
    st.title("📋 Cardápios")
    tab1, tab2 = st.tabs(["➕ Novo Cardápio", "📖 Meus Cardápios"])
    with tab1:
        pagina_novo_cardapio()
    with tab2:
        pagina_meus_cardapios()
