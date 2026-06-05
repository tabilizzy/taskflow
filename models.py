from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date

#user model
class User(SQLModel, table=True):
    __tablename__ = "taskflow_user"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(SQLModel):
    username: str
    email: str
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

# product model
class Project(SQLModel, table=True):
    __tablename__ = "project"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="taskflow_user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCreate(SQLModel):
    name: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="taskflow_user.id")


class ProjectPublic(SQLModel):
    id: int
    name:str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="taskflow_user")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Membership(SQLModel, table=True):
    __tablename__ = "membership"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="taskflow_user.id")
    project_id: int = Field(foreign_key="project.id")
    role: str = "member" # 'owner' | 'member'

class Task(SQLModel, table=True):
    __tablename__ = "task"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = "todo" # 'todo' | 'in_progress' | 'done'
    priority: str = "medium" # 'low' | 'medium' | 'high'
    due_date: Optional[date] = None
    project_id: int = Field(foreign_key="project.id")
    assignee_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_by: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Comment(SQLModel, table=True):
    __tablename__ = "comment"
    id: Optional[int] = Field(default=None, primary_key=True)
    body: str
    task_id: int = Field(foreign_key="task.id")
    author_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Token creation
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    # what the login endpoint returns

class TokenData(SQLModel):
    # what we extract from a token
    username: Optional[str] = None
