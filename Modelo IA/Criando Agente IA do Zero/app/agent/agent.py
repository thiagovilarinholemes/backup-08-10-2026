"""
Agente responsável por interpretar a solicitação
do usuário.

Nesta primeira versão utilizaremos regras simples.

Posteriormente podemos substituir essa camada
por um LLM da Hugging Face.
"""

import re


class ArticleAgent:
    """
    Agente responsável por interpretar solicitações
    relacionadas à pesquisa de artigos.
    """

    def process_request(
        self,
        request: str
    ) -> dict:
        """
        Interpreta a solicitação do usuário.

        Parameters
        ----------
        request:
            Solicitação escrita pelo usuário.

        Returns
        -------
        dict
            Configuração da pesquisa.
        """

        # Procura números dentro da frase.
        numbers = re.findall(
            r"\d+",
            request
        )

        # Caso o usuário informe uma quantidade,
        # utiliza essa quantidade.
        if numbers:

            limit = int(
                numbers[0]
            )

        # Caso contrário, utiliza 10 artigos.
        else:

            limit = 10

        # Remove a quantidade da frase.
        query = re.sub(
            r"\d+",
            "",
            request
        )

        # Remove palavras comuns.
        query = re.sub(
            r"\b(artigos?|pesquise|pesquisar|"
            r"encontre|buscar|busque|sobre|"
            r"quero|quero encontrar)\b",
            "",
            query,
            flags=re.IGNORECASE
        )

        # Remove espaços duplicados.
        query = re.sub(
            r"\s+",
            " ",
            query
        ).strip()

        # Retorna a configuração.
        return {
            "query": query,
            "limit": limit
        }