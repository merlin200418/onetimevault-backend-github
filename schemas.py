
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageCreate(BaseModel):
    encrypted_message: str

class MessageRead(BaseModel):
    id: str
    encrypted_message: str
