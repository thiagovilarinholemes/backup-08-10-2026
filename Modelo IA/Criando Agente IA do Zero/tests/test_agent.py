"""
Testes unitários do agente.
"""

from app.agent.agent import ArticleAgent


def test_agent_extracts_quantity():

    agent = ArticleAgent()

    result = agent._process_with_rules(
        "Quero 20 artigos sobre inteligência artificial"
    )

    assert result["limit"] == 20


def test_agent_extracts_query():

    agent = ArticleAgent()

    result = agent._process_with_rules(
        "Quero 20 artigos sobre Databricks"
    )

    assert "Databricks" in result["query"]