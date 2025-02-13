import src.agent.graph_structure.prompts as prompts
import langchain
from dotenv import load_dotenv
from src.agent.llm_utils.langchain_utils import get_llm
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage
from src.agent.graph_structure.tools import TOOLS
from src.audio.elevenlabs_utils import ElevenLabsUtils

load_dotenv(dotenv_path="../../../.env")
llm = get_llm()
elevenlabs_utils = ElevenLabsUtils()

def assistant(state: MessagesState):
    """
    This function represents the assistant node on graph, is a ReAct assistant.
    """

    llm_with_tools = llm.bind_tools(TOOLS)

    sys_msg = SystemMessage(
        content=prompts.ASSISTANT_PROMPT.format(input=state["messages"][-1].content)
    )

    result = llm_with_tools.invoke([sys_msg] + state["messages"])

    last_msg = result.content

    elevenlabs_utils.play_message(last_msg)

    return {"messages": [result]}