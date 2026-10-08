"""Este módulo é responsável por identificar problemas de qualidade
existentes em um DataFrame.

Principais verificações:

- Valores nulos
- Linhas duplicadas
- Colunas completamente vazias
- Linhas completamente vazias
- Percentual de valores nulos
- Colunas com alta quantidade de valores ausentes
"""

import pandas as pd
from pathlib import Path

caminho = Path("data") /("Games_Android_CSV") / "multilingual_mobile_app_reviews_2025.csv"
dataframe = pd.read_csv(caminho)  # Inicializa o DataFrame vazio


def validate_dataframe(dataframe: pd.DataFrame) -> None:

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

def count_nulls(dataframe: pd.DataFrame) -> dict:
    """
    Calcula a quantidade de valores nulos por coluna.

    Retorna
    -------
    dict
        Dicionário contendo a quantidade de nulos por coluna.
    """

    validate_dataframe(dataframe)

    nulls = dataframe.isnull().sum()

    return nulls.to_dict()


def calculate_null_percentage(dataframe: pd.DataFrame) -> dict:
    """
    Calcula o percentual de valores nulos por coluna.
    """

    validate_dataframe(dataframe)

    total_rows = len(dataframe)

    if total_rows == 0:
        return {}

    percentages = (
        dataframe.isnull().sum() / total_rows * 100
    ).round(2)

    return percentages.to_dict()


def find_columns_with_nulls(dataframe: pd.DataFrame) -> list:
    """
    Retorna somente as colunas que possuem valores nulos.
    """

    validate_dataframe(dataframe)

    nulls = dataframe.isnull().sum()

    return [
        column
        for column, quantity in nulls.items()
        if quantity > 0
    ]


def find_columns_completely_empty(dataframe: pd.DataFrame) -> list:
    """
    Identifica colunas onde todos os valores são nulos.
    """

    validate_dataframe(dataframe)

    return [
        column
        for column in dataframe.columns
        if dataframe[column].isnull().all()
    ]


def find_empty_rows(dataframe: pd.DataFrame) -> int:
    """
    Identifica quantas linhas possuem todos os valores nulos.
    """

    validate_dataframe(dataframe)

    return int(
        dataframe.isnull().all(axis=1).sum()
    )


def count_duplicates(dataframe: pd.DataFrame) -> int:
    """
    Conta a quantidade de linhas duplicadas.
    """

    validate_dataframe(dataframe)

    return int(
        dataframe.duplicated().sum()
    )


def calculate_duplicate_percentage(
    dataframe: pd.DataFrame,
) -> float:
    """
    Calcula o percentual de registros duplicados.
    """

    validate_dataframe(dataframe)

    total_rows = len(dataframe)

    if total_rows == 0:
        return 0.0

    duplicates = dataframe.duplicated().sum()

    return round(
        (duplicates / total_rows) * 100,
        2,
    )


def calculate_quality_score(
    dataframe: pd.DataFrame,
) -> float:
    """
    Calcula um indicador simples de qualidade.

    A pontuação começa em 100.

    Penalidades:

    - Valores nulos: até 50 pontos
    - Duplicidades: até 30 pontos
    - Linhas completamente vazias: até 20 pontos

    O resultado final fica entre 0 e 100.

    Observação:
    Esta pontuação é um indicador simplificado para o projeto.
    Ela não representa um padrão universal de Data Quality.
    """

    validate_dataframe(dataframe)

    total_cells = dataframe.shape[0] * dataframe.shape[1]

    if total_cells == 0:
        return 0.0

    null_cells = dataframe.isnull().sum().sum()

    null_percentage = (
        null_cells / total_cells
    ) * 100

    duplicate_percentage = calculate_duplicate_percentage(
        dataframe
    )

    empty_rows = find_empty_rows(dataframe)

    empty_row_percentage = (
        empty_rows / len(dataframe)
    ) * 100

    # Limita cada penalidade ao seu peso máximo.
    null_penalty = min(
        null_percentage,
        50,
    )

    duplicate_penalty = min(
        duplicate_percentage,
        30,
    )

    empty_row_penalty = min(
        empty_row_percentage,
        20,
    )

    score = (
        100
        - null_penalty
        - duplicate_penalty
        - empty_row_penalty
    )

    return round(
        max(0, score),
        2,
    )


def analyze_quality(
    dataframe: pd.DataFrame,
) -> dict:
    """
    Executa todas as verificações de qualidade.

    Esta é a principal função utilizada pelo agente.

    Retorna
    -------
    dict
        Resultado completo da análise.
    """

    validate_dataframe(dataframe)

    null_counts = count_nulls(dataframe)
    null_percentages = calculate_null_percentage(dataframe)

    columns_with_nulls = find_columns_with_nulls(
        dataframe
    )

    empty_columns = find_columns_completely_empty(
        dataframe
    )

    empty_rows = find_empty_rows(
        dataframe
    )

    duplicates = count_duplicates(
        dataframe
    )

    duplicate_percentage = calculate_duplicate_percentage(
        dataframe
    )

    quality_score = calculate_quality_score(
        dataframe
    )

    return {
        "total_rows": int(len(dataframe)),

        "total_columns": int(len(dataframe.columns)),

        "null_counts": null_counts,

        "null_percentages": null_percentages,

        "columns_with_nulls": columns_with_nulls,

        "empty_columns": empty_columns,

        "empty_rows": empty_rows,

        "duplicate_rows": duplicates,

        "duplicate_percentage": duplicate_percentage,

        "quality_score": quality_score,
    }


def generate_quality_insights(
    quality_result: dict,
) -> list[str]:
    """
    Gera insights determinísticos sobre a qualidade.

    O objetivo é fornecer informações objetivas antes
    que o LLM faça a interpretação final.
    """

    insights = []

    quality_score = quality_result.get(
        "quality_score",
        0,
    )

    if quality_score >= 90:
        insights.append(
            "O dataset apresenta boa qualidade geral."
        )

    elif quality_score >= 70:
        insights.append(
            "O dataset apresenta qualidade moderada "
            "e possui alguns pontos que precisam de atenção."
        )

    else:
        insights.append(
            "O dataset apresenta problemas relevantes "
            "de qualidade que devem ser investigados."
        )

    duplicate_rows = quality_result.get(
        "duplicate_rows",
        0,
    )

    if duplicate_rows > 0:
        insights.append(
            f"Foram encontrados {duplicate_rows} "
            "registros duplicados."
        )

    empty_columns = quality_result.get(
        "empty_columns",
        [],
    )

    if empty_columns:
        insights.append(
            "Existem colunas completamente vazias: "
            + ", ".join(empty_columns)
            + "."
        )

    columns_with_nulls = quality_result.get(
        "columns_with_nulls",
        [],
    )

    if columns_with_nulls:
        insights.append(
            "Existem valores nulos nas seguintes colunas: "
            + ", ".join(columns_with_nulls)
            + "."
        )

    empty_rows = quality_result.get(
        "empty_rows",
        0,
    )

    if empty_rows > 0:
        insights.append(
            f"Foram encontradas {empty_rows} "
            "linhas completamente vazias."
        )

    if not columns_with_nulls and duplicate_rows == 0:
        insights.append(
            "Não foram identificados valores nulos "
            "ou registros duplicados."
        )

    return insights


if __name__ == "__main__":
    # Exemplo de uso
    quality_result = analyze_quality(dataframe)
    insights = generate_quality_insights(quality_result)

    print("Resultado da Análise de Qualidade:")
    print(quality_result)
    print("\nInsights:")
    for insight in insights:
        print("-", insight)
