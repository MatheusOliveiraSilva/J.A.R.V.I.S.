from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import START, StateGraph, MessagesState
from langchain_core.messages import HumanMessage
from agent.nodes import assistant
from agent.tools import TOOLS
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
config = {"configurable": {"thread_id": '1'}}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(TOOLS))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# Compile graph
graph = builder.compile(checkpointer=memory)

if __name__ == "__main__":
    messages = [HumanMessage(
        content="Muda o dono da task 44 para eduardo")
    ]

    result = graph.invoke({"messages": messages}, config)

    for message in result["messages"]:
        print(message.content)
        print("--" * 50)
