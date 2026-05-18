# Interface layer — HTTP endpoints.
#
# This file defines the FastAPI router and maps HTTP verbs + paths to
# service function calls. It is the only layer that knows about HTTP.
#
# Rules:
# - Never call repository functions directly — always go through service
# - Catch ValueError from the service layer and raise HTTPException instead
# - Use Depends(get_db) to inject the database session
#
# This file should expose:
# - POST   /v1/users/          -> create a user
# - GET    /v1/users/          -> list users (with limit/offset pagination)
# - GET    /v1/users/{user_id} -> get one user by ID (404 if not found)
#
# See the README for the full implementation.


from fastapi import APIRouter, HTTPException
from app.database import get_db
from app import service
from app.schemas import UserCreate, UserOut, UserList

router = APIRouter(prefix="/v1/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=201)
def create_user(data: UserCreate):
    db = next(get_db())
    try:
        return service.add_user(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=UserList)
def list_users(limit: int = 20, offset: int = 0):
    db = next(get_db())
    try:
        return service.fetch_all_users(db, limit=limit, offset=offset)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str):
    db = next(get_db())
    try:
        return service.fetch_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))