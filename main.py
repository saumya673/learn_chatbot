from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAIError
from models import Message, PersonDetails
import uvicorn

from services.db.base import DBClient
from services.db.sqlite import SqliteDB
from services.llm_langchain import call_langchain_llm, call_structured_langchain_llm

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
async def chat(user_msg: Message):
    try:
        with SqliteDB() as db_client:
            msgs: list[Message] = db_client.get_chat_messages()

            llm_response: Message = await call_langchain_llm(msgs,user_msg)

            db_client.save_chat_messages(llm_response,user_msg)

        return {"message": llm_response.content}
    except OpenAIError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)
    

@app.post("/chat-structured")
async def chat(user_msg: Message) -> PersonDetails:
    try:
        my_story = "I had a great day"
        structured_output = await call_structured_langchain_llm(user_msg)
        print("llm ka result", structured_output)

        result: PersonDetails = PersonDetails(**structured_output.model_dump(), short_story=my_story)
        
        return result
    except OpenAIError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)



def main():
    uvicorn.run(app="main:app", reload=True)


if __name__ == "__main__":
    main()
