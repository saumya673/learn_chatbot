from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAIError
from langchain_openai import ChatOpenAI
from models import Message
import uvicorn

from services.db.base import DBClient
from services.db.sqlite import SqliteDB
from services.llm import call_llm

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
def chat(user_msg: Message):
    try:
        db_client: DBClient = SqliteDB()
        msgs: list[Message] = db_client.get_chat_messages()

        llm_response: Message = call_llm(msgs,user_msg)

        db_client.save_chat_messages(llm_response,user_msg)

        return {"message": llm_response.content}
    except OpenAIError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)

# @app.get("/chat-langchain")
# def chat_langchain(req: str):
#     try:
#         client = ChatOpenAI(api_key=openai_key,model="gpt-5.4-nano")

#         response = client.invoke(req)

#         return response.content
#     except OpenAIError as err:
#         raise HTTPException(status_code=err.status_code, detail=err.message)


def main():
    uvicorn.run(app="main:app", reload=True)


if __name__ == "__main__":
    main()
