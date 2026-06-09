from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date

class Task(SQLModel, table=True):
    __tablename__ = "task"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = "todo" # 'todo' | 'in_progress' | 'done'
    priority: str = "medium" # 'low' | 'medium' | 'high'
    due_date: Optional[date] = None
    project_id: int = Field(foreign_key="project.id")
    assignee_id: Optional[int] = Field(default=None, foreign_key="taskflow_user.id")
    created_by: int = Field(foreign_key="taskflow_user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    status: str = "todo" # 'todo' | 'in_progress' | 'done'
    priority: str = "medium" # 'low' | 'medium' | 'high'
    due_date: Optional[date] = None
    assignee_id: Optional[int] = Field(default=None, foreign_key="taskflow_user.id")
    created_by: int = Field(foreign_key="taskflow_user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
