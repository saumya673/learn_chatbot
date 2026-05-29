from models import Message, PersonDetailsLlm
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_key)

def call_llm(msgs: list[Message], user_msg: Message) -> Message:
    msgs.append(user_msg)
    llm_input = []

    for msg in msgs:
        llm_input.append(
            {
                "role": msg.role,
                "content": msg.content
            }
        )
    try:
        response = client.responses.create(
                model="gpt-5-nano",
                input=llm_input
            )
    except Exception as e:
        raise e
    
    return Message(id=response.id, role="assistant", content=response.output_text)


def call_structured_llm(user_msg):
    llm_input = [{
        "role": user_msg.role,
        "content": user_msg.content
    }]
    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=llm_input,
        text_format=PersonDetailsLlm
    )

    return response.output_parsed

    
