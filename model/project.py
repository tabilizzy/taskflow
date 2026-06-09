from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date

# project model
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

