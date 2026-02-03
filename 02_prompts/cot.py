from openai import OpenAI
from dotenv import load_dotenv
import json
load_dotenv()
client =  OpenAI()

SYSTEM_PROMPT ="""
    You are an expert AI assistant in resolving user queries using chain of thought 
    You work on START , PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input) ,PLAN (That can be multiple times
    ) and finally OUTPUT (which is going to be displayed to the user).

    Output JSON Format:
    {
        "step": "START" or "PLAN" or "OUTPUT",
        "thoughts": "string describing your thoughts",
        "action": "string describing the action to be taken" or null,
        "action_input": "string describing the input to the action" or null,
        "output": "final output string" or null
    }

    Example 1:
    START: hi , can you solve 2+3*5/10
    PLAN: To solve the expression, I need to follow the order of operations (PEMDAS).
    OUTPUT: The result of the expression 2+3*5/10 is 3.5

"""
print("="*30)
message_history = [
    {
        "role":"system",
        "content":SYSTEM_PROMPT
    },
]

user_query = input("Enter your query:  ")
message_history.append({
    "role":"user",
    "content":user_query
})

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type":"json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({
        "role":"assistant",
        "content":raw_result
    })

    parsed_result = json.loads(raw_result)
    if parsed_result.get("step")=="START":
        print(f"Start {parsed_result.get('thoughts')}")
        continue
    elif parsed_result.get("step")=="PLAN":
        print(f"Plan: {parsed_result.get('thoughts')}")
        continue
    elif parsed_result.get("step")=="OUTPUT":
        print(f"Output: {parsed_result.get('output')}")
        break
# response=client.chat.completions.create(
#     model="gpt-4o-mini",
#     response_format={"type":"json_object"},
#     messages=[
#         {
#             "role":"system",
#             "content":SYSTEM_PROMPT
#         },
#         {
#             "role":"user",
#             "content":"How's the weather today?"
#         },
#         {
#             "role":"assistant",
#             "content":json.dumps({
#                     "step": "START",
#                     "thoughts": "The user is asking for the current weather information. I need to gather the current weather data for their location.",
#                     "action":"",
#                     "action_input": "",
#                     "output": ""
#                 }
#     )},
#     {
#         "role":"assistant",
#         "content":json.dumps({"step": "PLAN", "thoughts": "To provide accurate weather information, I need to define the user's location as well as understand the type of weather details they want (temperature, conditions, etc.).", "action": "", "action_input": "", "output": ""})    }
#     ]
# )

# print(response.choices[0].message.content)