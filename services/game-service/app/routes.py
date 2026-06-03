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

from fastapi import APIRouter, HTTPException
from app.database import get_db
from app import service
from app.schemas import GameCreate, GameOut, GameList

router = APIRouter(prefix="/v1/games", tags=["games"])

@router.post("/", response_model=GameOut, status_code=201)
def create_game(data: GameCreate):
    db = next(get_db())
    try:
        return service.add_game(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=GameList)
def list_games(limit: int = 20, offset: int = 0):
    db = next(get_db())
    try:
        return service.fetch_all_games(db, limit=limit, offset=offset)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{game_id}", response_model=GameOut)
def get_game(game_id: str):
    db = next(get_db())
    try:
        return service.fetch_game(db, game_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

#
# Module 5 — CQRS: also add this endpoint (declare it before /{game_id}):
# - GET /v1/games/{game_id}/summary -> read from Redis cache (404 if not cached)
#   from app.infrastructure.cache import get_game_summary

