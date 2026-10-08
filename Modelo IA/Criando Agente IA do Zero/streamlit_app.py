"""
Interface web do Agente de IA.

Execute:

    streamlit run streamlit_app.py
"""

import streamlit as st

from app.agent.agent import ArticleAgent
from app.database.dynamodb import DynamoDBClient


# =========================================================
# Configuração da página
# =========================================================

st.set_page_config(

    page_title="AI Article Agent",

    page_icon="🤖",

    layout="wide"
)


# =========================================================
# Cabeçalho
# =========================================================

st.title(
    "🤖 AI Article Research Agent"
)

st.caption(
    "Hugging Face + Scrapy + DynamoDB + LocalStack"
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.header(
        "⚙️ Configurações"
    )

    quantity = st.number_input(

        "Quantidade de artigos",

        min_value=1,

        max_value=100,

        value=10
    )


# =========================================================
# Campo de pesquisa
# =========================================================

query = st.text_input(

    "🔎 O que você deseja pesquisar?",

    placeholder=(
        "Ex: artigos sobre inteligência artificial"
    )
)


# =========================================================
# Botão de pesquisa
# =========================================================

if st.button(
    "🚀 Executar pesquisa",
    use_container_width=True
):

    if not query:

        st.warning(
            "Digite uma pesquisa."
        )

        st.stop()

    # Cria o agente.
    agent = ArticleAgent()

    # Processa a solicitação.
    with st.spinner(
        "🤖 Interpretando pesquisa..."
    ):

        result = agent.process_request(
            f"{quantity} artigos sobre {query}"
        )

    # Mostra interpretação.
    st.success(
        "Pesquisa interpretada!"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Consulta",
            result["query"]
        )

    with col2:

        st.metric(
            "Quantidade",
            result["limit"]
        )


# =========================================================
# Artigos armazenados
# =========================================================

st.divider()

st.subheader(
    "📚 Artigos armazenados"
)


if st.button(
    "🔄 Atualizar"
):

    database = DynamoDBClient()

    articles = database.get_articles(
        limit=100
    )

    if not articles:

        st.info(
            "Nenhum artigo encontrado."
        )

    else:

        st.dataframe(
            articles,
            use_container_width=True
        )