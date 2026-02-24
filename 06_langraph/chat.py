from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph ,START,END

class State(TypedDict):
    messages:Annotated[list,add_messages]

def chatbot(state:State):
    print("\n\nInside chatbot:-  ",state)
    return {
        "messages":["Hi , this is a message from chatbot node"]
    }

def tool(state:State):
    print("\n\nInside tool:-  ",state)
    return {
        "messages":["Hi, this is a message from tool node"]
    }
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tool",tool)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","tool")
graph_builder.add_edge("tool",END)



graph = graph_builder.compile()
updated_state = graph.invoke(State({
    "messages":["Hi , My name is karthik"]
}))
print(updated_state)