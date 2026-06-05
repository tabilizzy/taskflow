from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import UserCreate, User, UserPublic, Token, UserLogin
from sqlmodel import Session, select
from database import get_session
from auth import hash_password, verify_password, create_access_token, get_current_user

# authentication
auth_router = APIRouter(prefix="/auth", tags=["authentication"])
@auth_router.post("/register", response_model=UserPublic, status_code=201)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    # Check username is not already taken
    existing = session.exec(select(User).where(User.username == user_in.username)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already registered")
    # Hash the password before storing
    user = User(
    username=user_in.username,
    email=user_in.email,
    hashed_password=hash_password(user_in.password),)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

#login

@auth_router.post("/login", response_model=Token)
def login(
    #form_data: UserLogin = Depends(),
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),):
# Look up the user
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    # Verify password — same error message whether user doesn't exist or password is wrong
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"},)
# Create and return a JWT token
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token)

# Protected route — only authenticated users can access
@auth_router.get("/me", response_model=list[User])
def list_users(session: Session = Depends(get_session),
            current_user: User = Depends(get_current_user),):
            # <-- protects the route

# Only return todos belonging to the current user
# Only return todos belonging to the current user
    return session.exec(
    #select(User)).all()
    select(User).where(User.id == current_user.id)).all()

# Unprotected route — anyone can access
@auth_router.get("/health")
def health_check():
    return {"status": "ok"}