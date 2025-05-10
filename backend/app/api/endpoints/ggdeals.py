# app/api/endpoints/ggdeals.py
from fastapi import APIRouter, Query, Path
from app.services.ggdeals_service import get_ggdeals_games, get_ggdeals_game_details

router = APIRouter(prefix="/ggdeals", tags=["GG.deals"])

@router.get("/games")
def fetch_ggdeals_games(
    #url: str = Query(default="https://gg.deals/games/", description="URL de búsqueda en GG.deals")
):
    url = "https://gg.deals/games/"
    return get_ggdeals_games(url)
'''
@router.get("/game-details")
def fetch_game_details(
    game_url: str = Query(..., description="URL completa del juego en GG.deals. Ej: https://gg.deals/game/cyberpunk-2077/")
):
    return get_ggdeals_game_details(game_url)
'''
@router.get("/game/{game_slug}")
def fetch_game_details(
    game_slug: str = Path(..., description="Slug del juego. Ej: 'the-elder-scrolls-iv-oblivion-remastered'")
):
    """
    Obtiene detalles de un juego específico usando su slug de GG.deals
    Ejemplo: /ggdeals/game/the-elder-scrolls-iv-oblivion-remastered
    """
    game_url = f"https://gg.deals/game/{game_slug}/"
    return get_ggdeals_game_details(game_url)
