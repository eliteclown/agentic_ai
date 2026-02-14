import json
from openai import OpenAI
from dotenv import load_dotenv
import requests
load_dotenv()

client = OpenAI()

def weather_agent(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%c+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Sorry, I couldn't fetch the weather information right now."

avaialble_tools ={
    "weather_agent": weather_agent
}

SYSTEM_PROMPT = """
You are an expert AI assistant in resolving user queries using chain of thought with tools.
You work on START, PLAN, ACTION, and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, you can TAKE ACTION by using a tool if needed.
Finally, you can give an OUTPUT based on the tool's response.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (that can be multiple times), ACTION (using tools), and finally OUTPUT (which is displayed to the user).
- When using a tool, specify which tool and what input to provide.

Output JSON Format:
{
    "step": "START" or "PLAN" or "ACTION" or "OUTPUT",
    "thoughts": "string describing your thoughts",
    "tool_name": "weather_agent" or null,
    "tool_input": "string describing the input to the tool" or null,
    "output": "final output string" or null
}

Available Tools:
- weather_agent: Get the weather in a city. Input format: city name (e.g., "New York")

Example:
START: What's the weather in London?
PLAN: The user wants to know the weather in London. I need to use the weather_agent tool to get this information.
ACTION: Call weather_agent with input "London"
OUTPUT: Based on the weather data, I can provide the user with the current weather in London.
"""



def main():
    user_query = input("> ")
    messages_history =[
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        }
    ]
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_history,
            response_format={"type":"json_object"}
        )

        raw_result = response.choices[0].message.content
        parsed_result = json.loads(raw_result)
        if parsed_result.get("step")=="START":
            print(f"User Query: {user_query}")
            messages_history.append(
                {
                "role":"user",
                "content": user_query
                }
            )
            continue
        elif parsed_result.get("step")=="PLAN":
            print(f"Thoughts: {parsed_result.get('thoughts')}")
            messages_history.append(
                {
                "role":"developer",
                "content": f"Thoughts: {parsed_result.get('thoughts')}"
                }
            )
            continue
        elif parsed_result.get("step")=="ACTION":
            print(f"Thoughts: {parsed_result.get('thoughts')}")
            print(f"Tool Name: {parsed_result.get('tool_name')}")
            print(f"Tool Input: {parsed_result.get('tool_input')}")
            tool_name = parsed_result.get("tool_name")
            tool_input = parsed_result.get("tool_input")
            tool_output = avaialble_tools[tool_name](tool_input)
            print(f"Tool Output: {tool_output}")
            messages_history.append(
                {
                "role":"developer",
                "content": f"Tool Output: {tool_output}"
                
                }
            )
            continue
        elif parsed_result.get("step")=="OUTPUT":
            messages_history.append(
                {
                "role":"developer",
                "content": f"Final Output: {parsed_result.get('output')}"
                }
            )
            print(f"Final Output: {parsed_result.get('output')}")
            break
        
        else:
            print("Invalid step")
        
main()
# def main():
#     user_query = input("> ")
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role":"user",
#                 "content":user_query            
#             }
#         ]
#     )

#     print(response.choices[0].message.content)

# main()