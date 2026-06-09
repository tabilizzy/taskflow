from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date


class Comment(SQLModel, table=True):
    __tablename__ = "comment"
    id: Optional[int] = Field(default=None, primary_key=True)
    body: str
    task_id: int = Field(foreign_key="task.id")
    author_id: int = Field(foreign_key="taskflow_user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CreateComment(SQLModel):
    body: str
    task_id: int = Field(foreign_key="task.id")
    author_id: int = Field(foreign_key="taskflow_user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)