from typing_extensions import TypedDict
from typing import Annotated,Optional,Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph ,START,END
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
class State(TypedDict):
    user_query:str
    llm_output:Optional[str]
    is_good:Optional[bool]

def chatbot(state:State):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"user",
                "content":state.get("user_query")
            }
        ]

    )
    state["llm_output"]=response.choices[0].message.content
    return state

def chatbot_gemini(state:State):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"user",
                "content":state.get("user_query")
            }
        ]

    )
    state["llm_output"]=response.choices[0].message.content
    return state

def endnode(state:State):
    return state

def eval(state:State)->Literal["chatbot_gemini","endnode"]:
    if True:
        return "endnode"
    return "chatbot_gemini"

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endnode",endnode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",eval)
graph_builder.add_edge("chatbot_gemini","endnode")
graph_builder.add_edge("endnode",END)

graph = graph_builder.compile()
updated_state = graph.invoke(State(
    {
        "user_query":"Hi,what is 2+2"
    }
))

print("\n\n upadted state:  ",updated_state)



