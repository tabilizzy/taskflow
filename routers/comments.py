from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from models import Comment, CreateComment
from auth import get_current_user, get_session, User
from sqlmodel import Session, select

task_router = APIRouter(prefix="/tasks", tags=["Comments"])

@task_router.get("/{task_id}/comments", response_model=list[Comment], status_code=status.HTTP_200_OK)
def get_task_comments(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    """Retrieve all comments associated with a specific task."""
    statement = select(Comment).where(Comment.task_id == task_id)
    comments = session.exec(statement).all()
    return comments

@task_router.post("/{task_id}/comments", response_model=list[Comment], status_code=status.HTTP_201_CREATED)
def create_comment_for_task(
    task_id: int,
    comment_in: CreateComment,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    """Add a new comment to a specific task."""
    # Convert the payload to our full database Table model [1]
    db_comment = Comment.model_validate(comment_in, update={"task_id": task_id})
    
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return [db_comment]

@task_router.delete("/{task_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment_from_task(
    task_id: int,
    comment_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    """Delete a specific comment from a task."""
    statement = select(Comment).where(Comment.task_id == task_id, Comment.id == comment_id)
    comment = session.exec(statement).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found on this task")
        
    session.delete(comment)
    session.commit()
    return None
