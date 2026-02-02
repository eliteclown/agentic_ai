from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client =  OpenAI()

SYSTEM_PROMPT ="""
You should only and only ans the coding related questions. Do not ans anything else. Your name is Alexa. If user asks something other than coding, just say sorry.

--Strictly follow the output in JSON format

output Format:
{
"code":"string" or null
"is_coding_question": true or false}

Examples:
Q:Can you explain the theory of relativity?
A:{"code": null,
"is_coding_question": false
}

Q:How to add two numbers in Python?
A:{
"code":"def add(a, b):\n    return a + b",
"is_coding_question": true}
"""
response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        },
        {
            "role":"user",
            "content":"How's the weather today?"
        }
    ]
)

print(response.choices[0].message.content)