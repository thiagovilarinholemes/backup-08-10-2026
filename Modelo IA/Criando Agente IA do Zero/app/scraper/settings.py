"""
Configurações globais do Scrapy.
"""

BOT_NAME = "agente_ia_artigos"


SPIDER_MODULES = [
    "app.scraper.spiders"
]


NEWSPIDER_MODULE = (
    "app.scraper.spiders"
)


# Respeita robots.txt.
ROBOTSTXT_OBEY = True


# Evita requisições excessivas.
DOWNLOAD_DELAY = 1


# Concorrência.
CONCURRENT_REQUESTS = 4


# User-Agent.
USER_AGENT = (
    "ArticleResearchBot/1.0"
)


# Pipeline responsável por persistência.
ITEM_PIPELINES = {

    "app.scraper.pipeline.DynamoDBPipeline": 300

}