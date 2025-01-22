import os
from itertools import chain
from app.agent.llm_utils.langchain_utils import get_llm
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../../.env")

llm = get_llm()

search_tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
)

SUMMARY_PROMPT = """
Você recebeu informações de várias fontes para responder a seguinte pergunta: {query}.
Use as informações fornecidas para criar um resumo coeso e claro.
Inclua links relevantes no final para referência.

Informações:
{documents}

Formato esperado de output:
------
Resumo:
< Resumo >
Referências:
< links relevantes >
------

Por favor, forneça um resumo e referências para a pergunta abaixo:
{query}
"""

def web_search(query: str) -> str:
    """
    Search the web for information on the given query.
    Args:
        query (str): The query to search for.
    """
    global search_tool
    search_results = search_tool.invoke(query)

    documents_string = f"\n".join([
        f"Content: {result['content']}\n\nReference URL: {result['url']}" for result in search_results
    ])

    prompt = SUMMARY_PROMPT.format(
        query=query,
        documents=documents_string
    )

    chain = llm | StrOutputParser()

    response = chain.invoke([HumanMessage(prompt)])

    return response