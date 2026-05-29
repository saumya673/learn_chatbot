from pydantic import BaseModel
from typing import Literal


class Message(BaseModel):
    id: str
    role: Literal["system","assistant","user","tool"]
    content: str


class PersonDetailsLlm(BaseModel):
    name: str
    age: int
    address: str

class PersonDetails(BaseModel):
    name: str
    age: int
    address: str
    short_story: str