import streamlit as st

from app.tools.data_loader import load_data
from app.tools.data_profiler import profile_dataframe

from app.analysis.quality import analyze_quality, generate_quality_insights


def main():

     # ========================================================
    # CONFIGURAÇÃO DA PÁGINA
    # =========================================================
    st.set_page_config(
            page_title="DataMind AI - Customized",
            page_icon="🤖",
            layout="wide",
        )

    # ========================================================
    # TÍTULO
    # ========================================================
    st.title("🤖 DataMind AI")

    st.markdown(
        """
        ### Agente Autônomo de Inteligência de Dados

        Carregue um arquivo e faça perguntas sobre
        seus dados utilizando linguagem natural.
        """
    )

    # ========================================================
    # UPLOAD DO ARQUIVO
    # ========================================================

    uploaded_file = st.file_uploader(
        "📂 Carregue seu arquivo",
        type=[
            "csv",
            "xlsx",
            "xls",
            "parquet",
        ],
    )

    # ========================================================
    # CASO NENHUM ARQUIVO TENHA SIDO CARREGADO
    # ========================================================

    if uploaded_file is None:

        st.info(
            "👆 Carregue um arquivo para começar "
            "a análise."
        )

        return
    
    # ========================================================
    # CARREGAMENTO DO ARQUIVO
    # ========================================================

    try:

        # Utiliza a função existente no data_loader.py.
        df = load_data(uploaded_file)

        st.success(
            f"Arquivo **{uploaded_file.name}** "
            "carregado com sucesso!"
        )

    except Exception as exc:

        st.error(
            f"Erro ao carregar o arquivo: {exc}"
        )

        return

    # ========================================================
    # INFORMAÇÕES GERAIS
    # ========================================================
    
    st.subheader("📊 Informações dos dados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    
    # --------------------------------------------------------
    # Registros
    # --------------------------------------------------------
    
    with col1:
    
        st.metric(
            "Registros",
            f"{df.shape[0]:,}",
        )
    
    
    # --------------------------------------------------------
    # Colunas
    # --------------------------------------------------------
    
    with col2:
    
        st.metric(
            "Colunas",
            f"{df.shape[1]:,}",
        )
    
    
    # --------------------------------------------------------
    # Valores nulos
    # --------------------------------------------------------
    
    with col3:
    
        st.metric(
            "Valores nulos",
            f"{int(df.isnull().sum().sum()):,}",
        )
    
    
    # --------------------------------------------------------
    # Duplicados
    # --------------------------------------------------------
    
    with col4:
    
        st.metric(
            "Duplicados",
            f"{int(df.duplicated().sum()):,}",
        )


    # ========================================================
    # ABAS
    # ========================================================

    (
        tab_agent,
        tab_profile,
        tab_quality,
        tab_statistics,
        tab_visualization,
        tab_data,
    ) = st.tabs(
        [
            "🤖 Agente IA",
            "🔎 Perfil",
            "🧹 Qualidade",
            "📈 Estatísticas",
            "📊 Visualizações",
            "📋 Dados",
        ]
    )


    # ========================================================
    # ABA QUALIDADE
    # ========================================================

    with tab_quality:

        st.subheader(
            "🧹 Qualidade dos dados"
        )
        ()

        try:

            quality = analyze_quality(df)
            insights = generate_quality_insights(quality)

            st.write("### 💡 Insights")

            for insight in insights:
                st.write(f"- {insight}")

            st.write("### 📊 Resultado da análise")

            st.json(quality)

        except Exception as exc:

            st.error(
                f"Erro ao analisar a qualidade: {exc}"
            )










if __name__ == "__main__":

    main()