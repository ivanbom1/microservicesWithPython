import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from app.database import SessionLocal, engine
from app.models import Base, Game
from datetime import datetime, timezone

def ts(x):
    return datetime.now(timezone.utc)

GAMES = [
    {"title": "Hollow Knight",            "genre": "Metroidvania", "platform": "PC/Switch/PS4/Xbox", "release_year": 2017, "cover_url": "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg",    "created_at": ts(1)},
    {"title": "Celeste",                  "genre": "Platformer",   "platform": "PC/Switch/PS4/Xbox", "release_year": 2018, "cover_url": "https://cdn.akamai.steamstatic.com/steam/apps/504230/header.jpg",    "created_at": ts(1)},
    {"title": "Hades",                    "genre": "Roguelite",    "platform": "PC/Switch/PS4/Xbox", "release_year": 2020, "cover_url": "https://cdn.akamai.steamstatic.com/steam/apps/1145360/header.jpg",   "created_at": ts(1)},
    {"title": "Stardew Valley",           "genre": "Simulation",   "platform": "PC/Switch/PS4/Xbox", "release_year": 2016, "cover_url": "https://cdn.akamai.steamstatic.com/steam/apps/413150/header.jpg",    "created_at": ts(1)},
    {"title": "Dead Cells",               "genre": "Roguelite",    "platform": "PC/Switch/PS4/Xbox", "release_year": 2018, "cover_url": "https://cdn.akamai.steamstatic.com/steam/apps/588650/header.jpg",    "created_at": ts(1)},
    {"title": "Ori and the Blind Forest", "genre": "Platformer",   "platform": "PC/Xbox",            "release_year": 2015, "cover_url": "https://cdn.akamai.steamstatic.com/steam/apps/261570/header.jpg",    "created_at": ts(1)},
    {"title": "Disco Elysium",            "genre": "RPG",          "platform": "PC/PS4/Xbox",        "release_year": 2019, "cover_url": "https://cdn.akamai.steamstatic.com/steam/apps/632470/header.jpg",    "created_at": ts(1)},
    {"title": "Outer Wilds",              "genre": "Adventure",    "platform": "PC/PS4/Xbox",        "release_year": 2019, "cover_url": "https://cdn.akamai.steamstatic.com/steam/apps/753640/header.jpg",    "created_at": ts(1)},
]

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    imported = 0
    for data in GAMES:
        existing = db.query(Game).filter(Game.title == data["title"]).first()
        if existing:
            continue
        game = Game(
            title=data["title"],
            genre=data["genre"],
            platform=data["platform"],
            release_year=data["release_year"],
            cover_url=data["cover_url"],
            created_at=data["created_at"]
        )
        db.add(game)
        imported += 1
    db.commit()
    db.close()
    print(f"Imported {imported} games.")

if __name__ == "__main__":
    run()