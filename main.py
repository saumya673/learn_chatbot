from re import I

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from models import Message
import uvicorn
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

messages: list[Message]  = []


@app.post("/chat")
def chat(user_msg: Message):
    try:
        #save user input to db
        messages.append(
            Message(id=user_msg.id, role=user_msg.role, content=user_msg.content)
        )

        # get msgs from db
        llm_input = []

        for msgs in messages:
            llm_input.append({
                "role": msgs.role, "content": msgs.content
            })

        # send all msgs to llm
        client = OpenAI(api_key=openai_key)
        response = client.responses.create(
            model="gpt-5-nano",
            input=llm_input
        )

        # save ai msg to db
        messages.append(
            Message(id=response.id, role="assistant", content=response.output_text)
        )

        print("list of messages",messages)
        return {"message": response.output_text}
    except OpenAIError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)

@app.get("/chat-langchain")
def chat_langchain(req: str):
    try:
        client = ChatOpenAI(api_key=openai_key,model="gpt-5.4-nano")

        response = client.invoke(req)

        return response.content
    except OpenAIError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)


def main():
    uvicorn.run(app="main:app", reload=True)
    


if __name__ == "__main__":
    main()
