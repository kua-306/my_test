from pydantic import BaseModel,field_validator
from typing import Optional,List


class UserCreate(BaseModel):
    username: str
    password: str
    @field_validator('username')
    @classmethod
    def validate_username(cls, username):
        if not username.strip():
            raise ValueError('Username cannot be empty')
        return username
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, password):
        if len(password) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if not password.strip():
            raise ValueError('Password cannot be empty')
        return password

class Questions(BaseModel):
    id: int
    question: str
    answer: str
    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True
class UserQ(User):
    questions: List[Questions]
    class Config:
        from_attributes = True


class QCreate(BaseModel):
    question: str
    answer: str

class Token(BaseModel):
    access_token: str
    token_type: str
    status : str

class TokenData(BaseModel):
    id : Optional[str] = None
