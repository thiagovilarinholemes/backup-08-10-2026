"""
Spider responsável por coletar resultados de pesquisa.

IMPORTANTE:

O Spider deve respeitar as políticas dos sites
visitados, robots.txt e limites de requisição.

A implementação abaixo utiliza uma fonte de pesquisa
HTML de exemplo para demonstrar a arquitetura.
"""

import hashlib
from datetime import datetime, timezone
from urllib.parse import quote

import scrapy

from app.models.article import Article


class ArticleSpider(scrapy.Spider):

    name = "article_spider"

    # Identifica o nosso crawler.
    custom_settings = {

        # Evita sobrecarregar o servidor.
        "DOWNLOAD_DELAY": 1,

        # Respeita robots.txt.
        "ROBOTSTXT_OBEY": True,

        # Limita concorrência.
        "CONCURRENT_REQUESTS": 4,

        # User-Agent identificável.
        "USER_AGENT":
            "ArticleResearchBot/1.0"
    }

    def __init__(
        self,
        query=None,
        limit=10,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        if not query:

            raise ValueError(
                "Informe uma consulta."
            )

        self.query = query

        self.limit = int(
            limit
        )

        self.count = 0

    def start_requests(self):

        encoded_query = quote(
            self.query
        )

        # Endpoint de pesquisa.
        url = (
            "https://www.google.com/search"
            f"?q={encoded_query}"
        )

        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    def parse(
        self,
        response
    ):

        # Processa os resultados.
        for result in response.css(
            "div.MjjYud"
        ):

            if self.count >= self.limit:

                break

            title = result.css(
                "h3::text"
            ).get()

            url = result.css(
                "a::attr(href)"
            ).get()

            description = " ".join(
                result.css(
                    "div.VwiC3b *::text"
                ).getall()
            )

            if not title or not url:

                continue

            # Cria ID baseado na URL.
            article_id = hashlib.sha256(
                url.encode(
                    "utf-8"
                )
            ).hexdigest()

            # Cria objeto.
            article = Article(

                article_id=article_id,

                title=title.strip(),

                url=url,

                description=(
                    description.strip()
                    if description
                    else None
                ),

                source="Google Search",

                search_query=self.query,

                collected_at=(
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                )
            )

            self.count += 1

            yield article.model_dump(
                mode="json"
            )