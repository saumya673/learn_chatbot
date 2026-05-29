from models import Message
from services.db.base import DBClient
import sqlite3


class SqliteDB(DBClient):
    def __init__(self):
        self.con = sqlite3.connect("chatbot.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS messages(id TEXT PRIMARY KEY, role TEXT, content TEXT)")
        self.con.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()

    def close(self):
        self.con.close()

    # get chat messages from db
    def get_chat_messages(self) -> list[Message]:
        cursor = self.cur
        cursor.execute("SELECT * FROM messages")
        all_rows = cursor.fetchall()

        chat_messages = []
        for row in all_rows:
            chat_messages.append(Message(id=row[0], role=row[1], content=row[2]))

        return chat_messages
    
    # save ai response and user msg to db
    def save_chat_messages(self,llm_response: Message, user_msg: Message):
        chat_messages = [
            (llm_response.id, llm_response.role, llm_response.content),
            (user_msg.id, user_msg.role, user_msg.content)
            ]

        self.cur.executemany("INSERT INTO messages (id, role, content) VALUES (?, ?, ?)", chat_messages)
        self.con.commit()

        
