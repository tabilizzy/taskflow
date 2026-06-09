from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional
from datetime import datetime, date

#user model
class User(SQLModel, table=True):
    __tablename__ = "taskflow_user"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: EmailStr =  Field(..., title="User Email", description="Must be a valid email address")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str
    #created_at: datetime = Field(default_factory=datetime.utcnow)

class UserLogin(SQLModel):
    username:str
    password:str

class UserPublic(SQLModel):
    id: int
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Membership(SQLModel, table=True):
    __tablename__ = "membership"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="taskflow_user.id")
    project_id: int = Field(foreign_key="project.id")
    role: str = "member" # 'owner' | 'member'

# Token creation
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    # what the login endpoint returns

class TokenData(SQLModel):
    # what we extract from a token
    username: Optional[str] = None