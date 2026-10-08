"""
DataMind AI - Data Profiler

Responsável por analisar a estrutura de um DataFrame.

O profiler identifica:

- Quantidade de registros
- Quantidade de colunas
- Nome das colunas
- Tipos de dados
- Colunas numéricas
- Colunas categóricas
- Colunas de data/hora
- Valores nulos
- Registros duplicados
"""

# ============================================================
# IMPORTAÇÕES
# ============================================================
# Biblioteca utilizada para manipulação e análise
# de estruturas de dados tabulares.
import pandas as pd
from pathlib import Path

# Para Testes Locais
# caminho = Path("data") /("House") / "House.csv"
# dataframe = pd.read_csv(caminho)  # Inicializa o DataFrame vazio

def validate_dataframe(
    dataframe: pd.DataFrame,
) -> None:
    """
    Valida se o objeto informado é um DataFrame e se não está vazio.

    Args:
        dataframe (pd.DataFrame): O DataFrame a ser validado.

    Raises:
        ValueError: Se o objeto informado não for um DataFrame ou se estiver vazio.
    """

    # --------------------------------------------------------
    # Verifica se o objeto é realmente um DataFrame.
    # --------------------------------------------------------
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("O objeto informado não é um DataFrame.")
    

    # --------------------------------------------------------
    # Verifica se o DataFrame possui registros.
    # --------------------------------------------------------
    if dataframe.empty or dataframe.dropna(how="all").empty:
        raise ValueError("O DataFrame está vazio.")
    
# ============================================================
# PERFIL COMPLETO DO DATAFRAME
# ============================================================
def profile_dataframe(
    dataframe: pd.DataFrame,
) -> dict:
    """
    Gera o perfil estrutural completo do DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dados que serão analisados.

    Returns
    -------
    dict
        Dicionário contendo as principais características
        estruturais do dataset.
    """

    # --------------------------------------------------------
    # Valida o DataFrame antes de iniciar a análise.
    # Função que valida se o objeto é um DataFrame e se não está vazio. 
    # --------------------------------------------------------
    validate_dataframe(dataframe)


    # ========================================================
    # COLUNAS NUMÉRICAS
    
    # Identifica automaticamente as colunas numéricas.
    # Os principais tipos que você pode usar são:
        # Tipo	        Descrição	            Exemplo
        # number	    Todos os números	    int, float
        # int	        Números inteiros	    10, 25, 100
        # float	        Números decimais	    10.5, 3.14
        # bool	        Booleanos	            True, False
        # object	    Texto/objetos	        "Python"
        # string	    Strings do Pandas	    "Python"
        # datetime	    Data e hora	            2026-09-06
        # timedelta	    Intervalos de tempo	    5 days
        # category	    Dados categóricos	    "SP", "TO"
    # ========================================================
    numeric_columns = (
            dataframe
            .select_dtypes(
                include=["number"]
            )
            .columns
            .tolist()
        )
    print("Colunas numéricas:", numeric_columns)


    # ========================================================
    # COLUNAS CATEGÓRICAS
    # ========================================================
    categorical_columns = []

    # Percorre todas as colunas do DataFra
    for column in dataframe.columns:
        # Obtém o tipo de dado da coluna.
        dtype = dataframe[column].dtype

        # ----------------------------------------------------
        # Verifica se a coluna possui dtype object.
        # ----------------------------------------------------
        is_object = (
            pd.api.types.is_object_dtype(dtype)
        )


    # ----------------------------------------------------
    # Verifica se a coluna possui dtype string.
    # ----------------------------------------------------
    # O teste de object é excluído para evitar que uma
    # mesma coluna seja identificada duas vezes.
    is_string = (
        pd.api.types.is_string_dtype(dtype)
        and not is_object
    )


    # ----------------------------------------------------
    # Verifica se a coluna possui dtype category.
    # ---------------------------------------------------
    # Utilizamos isinstance() em vez de
    # is_categorical_dtype().
    #
    # Isso evita warnings relacionados a funções
    # depreciadas em versões recentes do Pandas
    is_category = isinstance(
        dtype,
        pd.CategoricalDtype,
    )


    # ----------------------------------------------------
    # Classifica a coluna como categórica.
    # ----------------------------------------------------
    if (
        is_object
        or is_string
        or is_category
    ):
        categorical_columns.append(
            column
        )


    # ========================================================
    # COLUNAS DE DATA/HORA
    # ========================================================
    # Identifica colunas que possuem valores de data/hora.
    # São considerados:
    #
    # datetime
    # datetimetz
    #
    # O segundo representa datas que possuem informação
    # de timezone.
    datetime_columns = (
        dataframe
        .select_dtypes(
            include=[
                "datetime",
                "datetimetz",
            ]
        )
        .columns
        .tolist()
    )


    # ========================================================
    # VALORES NULOS
    # ========================================================
    # Calcula a quantidade de valores nulos
    # individualmente por coluna.

    null_values = (
        dataframe
        .isnull()
        .sum()
        .to_dict()
    )

    # --------------------------------------------------------
    # Converte os valores para int.
    #
    # Isso facilita a serialização para JSON e evita
    # objetos NumPy no resultado.
    # --------------------------------------------------------

    null_values = {
        column: int(value)
        for column, value
        in null_values.items()
    }


    # --------------------------------------------------------
    # Calcula a quantidade TOTAL de valores nulos.
    # --------------------------------------------------------

    null_total = int(
        dataframe
        .isnull()
        .sum()
        .sum()
    )

    # ========================================================
    # REGISTROS DUPLICADOS
    # ========================================================

    # Identifica a quantidade de linhas duplicadas.

    duplicated_rows = int(
        dataframe
        .duplicated()
        .sum()
    )

    # ========================================================
    # TIPOS DE DADOS
    # ========================================================

    # Cria um dicionário contendo o tipo de cada coluna.

    # O dtype é convertido para string porque isso facilita
    # a utilização dessas informações pelo agente de IA,
    # logs, JSON e interface Streamlit.

    dtypes = {
        column: str(dtype)
        for column, dtype
        in dataframe.dtypes.items()
    }


    # ========================================================
    # RESULTADO FINAL
    # ========================================================
    return {
    
        # ----------------------------------------------------
        # Quantidade de registros.
        # ----------------------------------------------------
        "rows": int(
            dataframe.shape[0]
        ),

    
        # ----------------------------------------------------
        # Quantidade de colunas.
        # ----------------------------------------------------
        "columns": int(
            dataframe.shape[1]
        ),

    
        # ----------------------------------------------------
        # Lista contendo os nomes das colunas.
        # ----------------------------------------------------
        "column_names": (
            dataframe
            .columns
            .tolist()
        ),

    
        # ----------------------------------------------------
        # Lista de colunas numéricas.
        # ----------------------------------------------------
        "numeric_columns": (
            numeric_columns
        ),

    
        # ----------------------------------------------------
        # Lista de colunas categóricas.
        # ----------------------------------------------------
        "categorical_columns": (
            categorical_columns
        ),

    
        # ----------------------------------------------------
        # Lista de colunas de data/hora.
        # ----------------------------------------------------
        "datetime_columns": (
            datetime_columns
        ),

    
        # ----------------------------------------------------
        # Tipos de dados de cada coluna.
        # ----------------------------------------------------
        "dtypes": dtypes,

    
        # ----------------------------------------------------
        # Valores nulos por coluna.
        #
        # Mantemos esta chave para compatibilidade com
        # componentes que utilizem "null_values".
        # ----------------------------------------------------
        "null_values": (
            null_values
        ),

    
        # ----------------------------------------------------
        # Valores nulos por coluna.
        #
        # Esta é a chave esperada pelos testes atuais:
        #
        # profile["null_by_column"]
        #
        # Ela possui exatamente os mesmos valores de
        # "null_values".
        # ----------------------------------------------------
        "null_by_column": (
            null_values
        ),

    
        # ----------------------------------------------------
        # Quantidade total de valores nulos.
        # ----------------------------------------------------
        "null_total": (
            null_total
        ),

    
        # ----------------------------------------------------
        # Quantidade de registros duplicados.
        # ----------------------------------------------------
        "duplicated_rows": (
            duplicated_rows
        ),
    }


# ============================================================
# COLUNAS NUMÉRICAS
# ============================================================

def get_numeric_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Retorna somente as colunas numéricas.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame que será analisado.

    Returns
    -------
    list[str]
        Lista contendo os nomes das colunas numéricas.
    """

    # Valida o DataFrame.
    validate_dataframe(dataframe)

    # Retorna somente os nomes das colunas numéricas.
    return (
        dataframe
        .select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )


# ============================================================
# COLUNAS CATEGÓRICAS
# ============================================================

def get_categorical_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Retorna as colunas categóricas do DataFrame.

    São consideradas categóricas:

    - object
    - string
    - category

    A identificação é feita individualmente por coluna
    para evitar warnings relacionados à migração de
    strings do Pandas.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame que será analisado.

    Returns
    -------
    list[str]
        Lista contendo os nomes das colunas categóricas.
    """

    # Valida o DataFrame.
    validate_dataframe(dataframe)

    # Lista onde serão armazenadas as colunas categóricas.
    categorical_columns = []

    # Percorre todas as colunas.
    for column in dataframe.columns:

        # Obtém o dtype da coluna.
        dtype = dataframe[column].dtype

        # ----------------------------------------------------
        # Verifica dtype object.
        # ----------------------------------------------------

        is_object = (
            pd.api.types.is_object_dtype(dtype)
        )

        # ----------------------------------------------------
        # Verifica dtype string.
        # ----------------------------------------------------

        is_string = (
            pd.api.types.is_string_dtype(dtype)
            and not is_object
        )

        # ----------------------------------------------------
        # Verifica dtype category.
        # ----------------------------------------------------

        is_category = isinstance(
            dtype,
            pd.CategoricalDtype,
        )

        # ----------------------------------------------------
        # Adiciona a coluna à lista caso seja categórica.
        # ----------------------------------------------------

        if (
            is_object
            or is_string
            or is_category
        ):
            categorical_columns.append(
                column
            )

    # Retorna as colunas categóricas.
    return categorical_columns


# ============================================================
# COLUNAS DE DATA/HORA
# ============================================================

def get_datetime_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Retorna somente as colunas de data/hora.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame que será analisado.

    Returns
    -------
    list[str]
        Lista contendo os nomes das colunas datetime.
    """

    # Valida o DataFrame.
    validate_dataframe(dataframe)

    # Retorna somente as colunas de data/hora.
    return (
        dataframe
        .select_dtypes(
            include=[
                "datetime",
                "datetimetz",
            ]
        )
        .columns
        .tolist()
    )






