"""
Agente de IA responsável por interpretar a solicitação
do usuário.

Exemplo:

    "Quero 20 artigos sobre inteligência artificial"

O agente deverá produzir:

    query = "inteligência artificial"
    limit = 20
"""

import json
import os
import re

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()


class ArticleAgent:
    """
    Agente responsável por interpretar solicitações.
    """

    def __init__(self):
        """
        Inicializa o cliente Hugging Face.
        """

        # Token da API.
        token = os.getenv(
            "HF_TOKEN"
        )

        # Modelo configurado.
        self.model = os.getenv(
            "HF_MODEL",
            "Qwen/Qwen2.5-3B-Instruct"
        )

        # Cliente Hugging Face.
        self.client = InferenceClient(
            api_key=token
        )

    def process_request(
        self,
        request: str
    ) -> dict:
        """
        Interpreta uma solicitação.

        Caso o modelo não esteja disponível,
        utilizamos um fallback baseado em regras.
        """

        try:

            return self._process_with_llm(
                request
            )

        except Exception as error:

            print(
                f"LLM indisponível: {error}"
            )

            return self._process_with_rules(
                request
            )

    def _process_with_llm(
        self,
        request: str
    ) -> dict:
        """
        Processa a solicitação usando o modelo
        da Hugging Face.
        """

        prompt = f"""
Você é um agente especializado em pesquisa
de artigos na internet.

Analise a solicitação abaixo:

{request}

Retorne SOMENTE JSON válido.

Formato obrigatório:

{{
    "query": "termo de pesquisa",
    "limit": 10
}}

Regras:

1. query deve conter o nome ou frase pesquisada.
2. limit deve ser um número inteiro.
3. Se a quantidade não for informada, use 10.
"""

        response = self.client.chat_completion(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            max_tokens=200,

            temperature=0
        )

        content = response.choices[
            0
        ].message.content

        # Localiza o JSON.
        match = re.search(
            r"\{.*\}",
            content,
            re.DOTALL
        )

        if not match:

            raise ValueError(
                "O modelo não retornou JSON válido."
            )

        result = json.loads(
            match.group()
        )

        # Validação mínima.
        if "query" not in result:

            raise ValueError(
                "Campo query ausente."
            )

        if "limit" not in result:

            result["limit"] = 10

        result["limit"] = int(
            result["limit"]
        )

        return result

    def _process_with_rules(
        self,
        request: str
    ) -> dict:
        """
        Fallback utilizado caso o modelo não esteja
        disponível.
        """

        # Procura números.
        numbers = re.findall(
            r"\d+",
            request
        )

        # Define quantidade.
        limit = (
            int(numbers[0])
            if numbers
            else 10
        )

        # Remove números.
        query = re.sub(
            r"\d+",
            "",
            request
        )

        # Remove palavras comuns.
        query = re.sub(
            r"\b("
            r"artigos?|"
            r"pesquise|"
            r"pesquisar|"
            r"encontre|"
            r"buscar|"
            r"busque|"
            r"sobre|"
            r"quero|"
            r"encontrar"
            r")\b",
            "",
            query,
            flags=re.IGNORECASE
        )

        # Normaliza espaços.
        query = re.sub(
            r"\s+",
            " ",
            query
        ).strip()

        return {
            "query": query,
            "limit": limit
        }