"""
Responsável por executar o Spider programaticamente.
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from app.scraper.spiders.article_spider import (
    ArticleSpider
)


class ScraperRunner:
    """
    Executa o processo de scraping.
    """

    def run(
        self,
        query: str,
        limit: int
    ):
        """
        Executa o Spider.

        Retorna os artigos coletados.
        """

        results = []

        # Configurações do Scrapy.
        settings = get_project_settings()

        # Cria processo.
        process = CrawlerProcess(
            settings
        )

        # Executa o Spider.
        process.crawl(
            ArticleSpider,
            query=query,
            limit=limit
        )

        process.start()

        return results