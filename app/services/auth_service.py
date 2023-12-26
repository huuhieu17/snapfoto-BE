# File: app/services/user_service.py
from jose import JWTError, jwt
from app.model.user import User
from app.model.token import TokenData
from app.db import get_database
from app.utils.security import verify_password, get_password_hash
from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.constants.jwt import oauth2_scheme, SECRET_KEY, ALGORITHM


async def get_user(username: str):
    db = get_database()
    user = await db.users.find_one({"username": username})
    return user

async def register_user(user: User):
    db = get_database()
   # Check if the username or email is already taken
    existing_user = await db.users.find_one({"$or": [{"username": user.username}, {"email": user.email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Hash the password before storing it
    user.password = get_password_hash(user.password)
    
    # Insert the user into the database
    await db.users.insert_one(user.dict())

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    if(token_data.username is None):
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
