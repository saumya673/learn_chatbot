from pydantic import BaseModel
from typing import Literal


class Message(BaseModel):
    id: str
    role: Literal["system","assistant","user","tool"]
    content: str


