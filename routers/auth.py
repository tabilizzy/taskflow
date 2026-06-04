from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import UserCreate, User, UserPublic, Token, UserLogin
from sqlmodel import Session, select
from database import get_session
from auth import hash_password, verify_password, create_access_token

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