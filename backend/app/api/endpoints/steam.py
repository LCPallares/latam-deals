# app/api/endpoints/steam.py
from fastapi import APIRouter, Query
from app.services.steam_service import get_steam_game_list, get_steam_game_details

router = APIRouter(prefix="/steam", tags=["Steam"])

@router.get("/games")
def search_steam_games(search: str = Query(None)):
    """Busca juegos en la tienda de Steam.
    ej: http://localhost:8000/steam/games?search=cyberpunk
    Response body:
    [
      {"appid": 1091500, "name": "Cyberpunk 2077"},
      {"appid": 123456, "name": "Cyberpunk Adventure"}
    ]
    """
    return get_steam_game_list(search)

@router.get("/game/{app_id}")
def get_game_details(app_id: int, pais_code: str = "CO"):
    return get_steam_game_details(app_id, pais_code)
