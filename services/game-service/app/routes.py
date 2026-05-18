# Interface layer — HTTP endpoints.
#
# Define a router with prefix="/v1/games" and implement these endpoints:
# - POST   /v1/games/          -> create a game (201)
# - GET    /v1/games/          -> list games (limit/offset pagination)
# - GET    /v1/games/search    -> search games by title (?q=...)
# - GET    /v1/games/{game_id} -> get one game by ID (404 if not found)
#
# IMPORTANT: declare /search BEFORE /{game_id} in your router.
# If /{game_id} comes first, FastAPI will try to match "search" as an ID
# and return a 422 Unprocessable Entity error.

from fastapi import APIRouter                             
                                                                                                                  
router = APIRouter(prefix="/v1/game", tags=["game"])
                                                                                                                  
@router.post("/", status_code=201)                        
def create_user():
    return {"message": "create game — not implemented yet"}
                                                                                                                  
@router.get("/")
def list_users():                                                                                               
    return {"items": [], "total": 0, "limit": 20, "offset": 0, "message": "games will be displayed here ..."}
                                                                                                                  
@router.get("/{game_id}")
def get_user(game_id: str):                                                                                     
    return {"message": f"get game {game_id} — not implemented yet"}   