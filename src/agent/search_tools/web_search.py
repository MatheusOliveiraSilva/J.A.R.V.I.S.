import os
from itertools import chain
from src.agent.llm_utils.langchain_utils import get_llm
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

    response = "Abaixo está o resultado da busca na web: \n" + documents_string

    return response