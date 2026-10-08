"""
Ponto de entrada da aplicação.

O usuário informa uma solicitação.

Exemplo:

    Quero 10 artigos sobre inteligência artificial
"""

from app.agent.agent import ArticleAgent


def main():
    """
    Executa o agente.
    """

    # Cria uma instância do agente.
    agent = ArticleAgent()

    # Solicita uma pesquisa ao usuário.
    request = input(
        "Digite sua pesquisa: "
    )

    # Processa a solicitação.
    result = agent.process_request(
        request
    )

    # Exibe a interpretação.
    print("\nPesquisa interpretada:")
    print(
        f"Consulta: {result['query']}"
    )

    print(
        f"Quantidade: {result['limit']}"
    )


# Executa o programa.
if __name__ == "__main__":
    main()