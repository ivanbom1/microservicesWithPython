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


from fastapi import APIRouter                             
                                                                                                                  
router = APIRouter(prefix="/v1/users", tags=["users"])
                                                                                                                  
@router.post("/", status_code=201)                        
    
def create_user():
    return {"message": "create user — not implemented yet"}
                                                                                                                  
@router.get("/")
def list_users():                                                                                               
    return {"items": [], "total": 0, "limit": 20, "offset": 0, "message": "users will be displayed here ..."}
                                                                                                                  
@router.get("/{user_id}")
def get_user(user_id: str):                                                                                     
    return {"message": f"get user {user_id} — not implemented yet"}   