from mem0 import Memory
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
load_dotenv()

client = OpenAI()
config = {
    "version":"v1.1",
    "embedder":{
        "provider":"openai",
        "config":{"api_key":OPENAI_API_KEY,"model":"text-embedding-3-small"}
    },
    "llm":{
        "provider":"openai",
        "config":{"api_key":OPENAI_API_KEY,"model":"gpt-4.1"}
    },
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host":"localhost",
            "port":6333
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_input =  input("> ")
    
    search_memory = mem_client.search(query=user_input,user_id="karthik")
    memories = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" for mem in search_memory.get("results")
    ]

    SYSTEM_PROMPT=f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """

    print("found memoeires:  ",memories)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
            "role":"user",
            "content":user_input
            }
        ]
    )
    
    ai_response = response.choices[0].message.content

    print("Ai response: ",ai_response)

    mem_client.add(
        user_id="karthik",
        messages=[
        
            {
                "role":"user",
                "content":user_input
            },
            {
                "role":"assistant",
                "content":ai_response
            }
        ]
    )