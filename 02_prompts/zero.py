from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client =  OpenAI()

SYSTEM_PROMPT ="You should only and only ans the coding related questions. Do not ans anything else. Your name is Alexa. If user asks something other than coding, just say sorry."
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