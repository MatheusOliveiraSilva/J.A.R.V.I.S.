from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import START, StateGraph, MessagesState
from langchain_core.messages import HumanMessage
from app.agent.graph_structure.nodes import assistant
from app.agent.graph_structure.tools import TOOLS
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

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
    config = {"configurable": {"thread_id": '1'}}

    messages = [HumanMessage(
        content="Muda o dono da task 1 para eduardo")
    ]

    result = graph.invoke({"messages": messages}, config)

    for message in result["messages"]:
        print(message.content)
        print("--" * 50)