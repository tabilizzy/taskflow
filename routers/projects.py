from fastapi import APIRouter, Depends, HTTPException
from models import User, Project, ProjectCreate, ProjectPublic
from sqlmodel import Session, select
from database import get_session
from auth import  get_current_user


# Protected route — only authenticated users can access
pro_router = APIRouter(prefix="/pro", tags=["project"])
@pro_router.get("/", response_model=list[ProjectPublic], status_code =201)
def list_products(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),):
# Only return product belonging to the current user
    statement = select(Project).where(Project.owner_id == current_user.id)
    projects = session.exec(statement).all()
    return projects

@pro_router.post("/", response_model=list[ProjectPublic], status_code =201)
def create_product(
    project_in: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    ):
    db_project = Project.model_validate(project_in)
    db_project.owner_id = current_user.id

    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return [db_project]
    
@pro_router.get("/{project_id}", response_model=list[ProjectPublic], status_code =200)
def list_products(
    project_id:int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),):
    project = session.get(Project, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Project not found")
    return [project]


@pro_router.put("/{project_id}",response_model=list[ProjectPublic], status_code =200)
def update_project(
    project_id:int,
    name:str,
    description:str,
    db:Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):

    project =db.query(Project).filter(Project.id == project_id).first()

    if project.owner_id == current_user.id:

        if not project:
            raise HTTPException(status=404, details="Todo not found")
        project.name = name
        project.description = description
        db.commit()
        db.refresh(project)
        return [project]
    raise HTTPException(status_code = 403, detail ="project not found")

@pro_router.delete("/{project_id}", status_code = 204)
def delete_todo(
    project_id:int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="project not found")
    db.delete(project)
    db.commit()
    return{
        "message":"project deleted"
    }