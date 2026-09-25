# NutriCardápio — Dashboard

Sua lógica original (banco de dados, cálculo nutricional, receitas e cardápios)
continua exatamente igual — só foi adicionada uma interface visual (`app.py`)
no lugar do menu de texto do `main.py`. O `main.py` continua funcionando
normalmente pelo terminal, se você quiser.

## 1. Instalar as dependências (só precisa fazer uma vez)

Abra o terminal **dentro da pasta `NutriCardapio`** e rode:

```
pip install -r requirements.txt
```

## 2. Rodar o dashboard

Ainda dentro da pasta `NutriCardapio`, rode:

```
streamlit run app.py
```

Isso vai abrir automaticamente uma aba no seu navegador com o dashboard
(normalmente em `http://localhost:8501`). Para parar, volte ao terminal e
aperte `Ctrl + C`.

## O que tem no dashboard

- **🏠 Início** — visão geral: quantos alimentos, receitas e cardápios você tem.
- **🔍 Alimentos** — pesquisa por nome e calculadora de quantidade (gramas → calorias/macros).
- **🍳 Receitas** — criar receita somando ingredientes, ver/editar/excluir receitas salvas.
- **📋 Cardápios** — montar cardápio com refeições (café, almoço, jantar...), cada uma
  podendo ter alimentos avulsos e/ou receitas prontas. Também dá pra ver/editar/excluir.

## Estrutura (nada mudou, só foi adicionado)

```
NutriCardapio/
├── app.py              <- NOVO: o dashboard (rode este arquivo)
├── main.py              (menu antigo em texto, continua funcionando)
├── requirements.txt     <- NOVO
├── alimentos/
├── receitas/
├── cardapios/
├── banco/
│   └── nutricardapio.db   (seus 597 alimentos da TACO, intactos)
└── dados/
```

## Dica

Se no futuro quiser distribuir isso para rodar em outro PC sem precisar
digitar comando nenhum, dá pra criar um atalho/arquivo `.bat` (Windows) que
já chama `streamlit run app.py` sozinho. É só avisar que eu monto isso.
