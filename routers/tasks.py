from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from models import Task, TaskCreate
from sqlmodel import Session, select
from database import get_session
from auth import get_current_user, User

proj_router = APIRouter(prefix="/project", tags=["Task"])

@proj_router.get("/{project_id}/tasks", response_model = list[Task], status_code = status.HTTP_200_OK)
def get_project_tasks(
    project_id: int,
    session: Session = Depends(get_session),
    current_user:User = Depends(get_current_user), ):
    """Retrieve all tasks belonging to a specific project."""
    tasks = session.exec(select(Task).where(Task.project_id == project_id)).all()
    return tasks

@proj_router.post("/{project_id}/tasks", response_model = list[Task], status_code =status.HTTP_201_CREATED)
def create_task_for_project(
    project_id: int,
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    # Convert validation model to full DB Table model
    db_task = Task.model_validate(task_in)
    db_task.project_id = project_id
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return [db_task]

@proj_router.get("/{project_id}/tasks/{task_id}", response_model = list[Task], status_code = status.HTTP_200_OK)
def get_single_task(
    project_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    statement = select(Task).where(Task.project_id == project_id, Task.id == task_id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return [task]


@proj_router.put("/{project_id}/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(
    project_id: int,
    task_id: int,
    task_update: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    """Perform a partial update on a task. Only provided fields change."""
    statement = select(Task).where(Task.project_id == project_id, Task.id == task_id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # exclude_unset=True ignores fields the user left out of their request
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@proj_router.delete("/{project_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    project_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    statement = select(Task).where(Task.project_id == project_id, Task.id == task_id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    session.delete(task)
    session.commit()
    return None