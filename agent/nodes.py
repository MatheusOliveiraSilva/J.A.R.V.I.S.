import agent.prompts as prompts
import langchain
from dotenv import load_dotenv
from llm_utils.langchain_utils import get_llm
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage
from agent.tools import TOOLS

load_dotenv()
llm = get_llm()

def assistant(state: MessagesState):
    """
    This function representes the single node on graph, is a ReAct assistant.
    """

    llm_with_tools = llm.bind_tools(TOOLS)

    sys_msg = SystemMessage(
        content=prompts.ASSISTANT_PROMPT.format(input=state["messages"][-1].content)
    )

    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}
