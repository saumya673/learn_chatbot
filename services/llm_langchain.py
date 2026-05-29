from models import Message, PersonDetailsLlm
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

client = ChatOpenAI(
    model="gpt-5-mini"
)

async def call_langchain_llm(msgs: list[Message],user_msg: Message) -> Message:
    msgs.append(user_msg)
    llm_input = [SystemMessage(content="You are a helpful friend.")]
    for msg in msgs:
        if msg.role == "assistant":
          llm_input.append(AIMessage(content=msg.content)),
        else:
            llm_input.append(HumanMessage(content=msg.content)),

    response = await client.ainvoke(llm_input)
    return Message(id=response.id, role="assistant", content=response.text)


async def call_structured_langchain_llm(user_msg: Message) -> PersonDetailsLlm:
    client_with_structure = client.with_structured_output(PersonDetailsLlm)
    response = client_with_structure.invoke(user_msg.content)
    return response
