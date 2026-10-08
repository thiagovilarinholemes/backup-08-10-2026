"""
Camada de acesso ao DynamoDB.

Toda comunicação com o banco fica centralizada
neste módulo.

Isso evita espalhar chamadas boto3 pelo projeto.
"""

import os
from typing import Optional

import boto3

from dotenv import load_dotenv


# Carrega as variáveis do arquivo .env.
load_dotenv()


class DynamoDBClient:
    """
    Cliente responsável pelas operações no DynamoDB.
    """

    def __init__(self):
        """
        Inicializa a conexão.
        """

        # Obtém as configurações.
        endpoint = os.getenv(
            "DYNAMODB_ENDPOINT"
        )

        region = os.getenv(
            "AWS_DEFAULT_REGION",
            "us-east-1"
        )

        # Cria o recurso DynamoDB.
        self.dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=endpoint,
            region_name=region,
            aws_access_key_id=os.getenv(
                "AWS_ACCESS_KEY_ID",
                "test"
            ),
            aws_secret_access_key=os.getenv(
                "AWS_SECRET_ACCESS_KEY",
                "test"
            )
        )

        # Nome da tabela.
        self.table_name = os.getenv(
            "DYNAMODB_TABLE",
            "articles"
        )

        # Referência para a tabela.
        self.table = self.dynamodb.Table(
            self.table_name
        )

    def save_article(self, article):
        """
        Insere ou atualiza um artigo.
        """

        # Converte o Pydantic para dict.
        item = article.model_dump(
            mode="json"
        )

        # Salva no DynamoDB.
        self.table.put_item(
            Item=item
        )

    def save_articles(self, articles):
        """
        Salva vários artigos utilizando batch_writer.

        O batch_writer é mais eficiente para inserções
        em lote.
        """

        with self.table.batch_writer() as batch:

            for article in articles:

                batch.put_item(
                    Item=article.model_dump(
                        mode="json"
                    )
                )

    def get_articles(
        self,
        limit: int = 100
    ):
        """
        Retorna artigos armazenados.
        """

        response = self.table.scan(
            Limit=limit
        )

        return response.get(
            "Items",
            []
        )

    def search_articles(
        self,
        query: str,
        limit: int = 100
    ):
        """
        Pesquisa artigos pelo termo.

        Como estamos usando LocalStack/DynamoDB sem
        um índice de texto, fazemos uma leitura e
        filtragem no lado da aplicação.

        Em uma versão futura podemos utilizar OpenSearch
        ou outro mecanismo de busca.
        """

        response = self.table.scan()

        items = response.get(
            "Items",
            []
        )

        query_lower = query.lower()

        results = []

        for item in items:

            title = item.get(
                "title",
                ""
            ).lower()

            description = item.get(
                "description",
                ""
            ).lower()

            if (
                query_lower in title
                or query_lower in description
            ):

                results.append(item)

            if len(results) >= limit:
                break

        return results

    def delete_all(self):
        """
        Remove todos os artigos da tabela.
        """

        response = self.table.scan()

        items = response.get(
            "Items",
            []
        )

        with self.table.batch_writer() as batch:

            for item in items:

                batch.delete_item(
                    Key={
                        "article_id":
                            item["article_id"]
                    }
                )