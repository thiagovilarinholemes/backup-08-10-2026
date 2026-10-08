"""
DataMind AI - Data Loader

Responsável pelo carregamento de arquivos de dados.
"""

# ============================================================
# IMPORTAÇÕES
# ============================================================
from pathlib import Path
import pandas as pd

# ============================================================
# FUNÇÃO DE CARREGAMENTO DE DADOS 
# ============================================================
def load_data(file_source) -> pd.DataFrame:
    """
        Carrega dados a partir de um caminho de arquivo
        ou de um objeto enviado pelo Streamlit.

        Parâmetros
        ----------
        file_source
            Caminho do arquivo ou objeto de upload.

        Retorno
        -------
        pd.DataFrame
            DataFrame contendo os dados.
    """

    # Se for um objeto semelhante ao arquivo do Streamlit,
    # utilizamos o nome para descobrir a extensão.
    # A função hasattr() em Python verifica se um objeto possui um determinado atributo ou método. 
    if hasattr(file_source, "name"):

        file_name = file_source.name

    else:

        file_name = str(file_source)

    # Obtém a extensão.
    extension = Path(file_name).suffix.lower()

    # -----------------------------------------------------
    # CSV
    # -----------------------------------------------------

    if extension == ".csv":

        return pd.read_csv(file_source)

    # -----------------------------------------------------
    # Excel
    # -----------------------------------------------------

    if extension in {".xlsx", ".xls"}:

        return pd.read_excel(file_source)

    # -----------------------------------------------------
    # Parquet
    # -----------------------------------------------------

    if extension == ".parquet":

        return pd.read_parquet(file_source)

    # -----------------------------------------------------
    # Formato não suportado
    # -----------------------------------------------------

    raise ValueError(
        f"Formato não suportado: {extension}. "
        "Use CSV, XLSX, XLS ou Parquet."
    )


