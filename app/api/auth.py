from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import get_current_user, register_user, authenticate_user
from app.model.user import User
from app.utils.security import login_for_access_token

router = APIRouter()
@router.post("/register", tags=["auth"])
async def register(username: str, password: str, email: str):
    await register_user(User(username=username, password=password, email=email ))
    return {"message": "User registered successfully"}

@router.post("/login", tags=["auth"])
async def login(username: str, password: str):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Call the service function to create a JWT token
    token = login_for_access_token(user)
    return token

@router.post("/token", include_in_schema=False, tags=["auth"])
async def authSwagger(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Call the service function to create a JWT token
    token = login_for_access_token(user)
    return token

@router.get("/me", response_model=User, tags=["auth"])
async def getCurrentUser(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.get("/test")
def hello_world(current_user: Annotated[User, Depends(get_current_user)]):
    return {"hello": "world"}