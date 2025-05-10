# app/services/ggdeals_service.py
from typing import Dict, List
from app.scrapers.ggdeals import scrape_ggdeals_list, scrape_ggdeals_game_details

def get_ggdeals_games(url: str = "https://gg.deals/games/") -> Dict:
    """Para listado de juegos"""
    try:
        games = scrape_ggdeals_list(url)
        return {
            "success": True,
            "count": len(games),
            "data": games,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": []
        }

def get_ggdeals_game_details(game_url: str) -> Dict:
    """Para detalles de un juego específico"""
    try:
        details = scrape_ggdeals_game_details(game_url)
        return {
            "success": True,
            "data": details,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }
