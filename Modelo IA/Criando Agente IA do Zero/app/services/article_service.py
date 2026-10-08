"""
Camada de serviço responsável por coordenar:

Agente
    ↓
Scrapy
    ↓
DynamoDB
"""

from app.agent.agent import ArticleAgent
from app.database.dynamodb import DynamoDBClient
from app.scraper.spiders.article_spider import (
    ArticleSpider
)


class ArticleService:
    """
    Serviço principal da aplicação.
    """

    def __init__(self):

        self.agent = ArticleAgent()

        self.database = DynamoDBClient()

    def search(
        self,
        request: str
    ):
        """
        Executa uma pesquisa completa.
        """

        # Primeiro o agente interpreta
        # a solicitação.
        config = self.agent.process_request(
            request
        )

        # Retorna a configuração interpretada.
        return config