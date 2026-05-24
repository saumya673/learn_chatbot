from abc import ABC, abstractmethod
from models import Message


class DBClient(ABC):
    @abstractmethod
    def get_chat_messages(self) -> list[Message]:
        pass
    
    @abstractmethod
    def save_chat_messages(self,llm_response: Message, user_msg: Message):
        pass

