# app/services/steam_service.py
import requests
from typing import Optional, Dict, Any

STEAM_API_BASE = "https://api.steampowered.com"
#STEAM_API_BASE = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
#STEAM_STORE_BASE = "https://store.steampowered.com/api"
STEAM_STORE_BASE = "https://store.steampowered.com/api/appdetails"

def get_steam_game_list(search: Optional[str] = None) -> list:
    """Obtiene lista de juegos de Steam. Ejemplo sin API key.
    {"appid":2461320,"name":"Grocery Grab Demo"},{"appid":2461340,"name":"Feluna Base"}
    """
    url = f"{STEAM_API_BASE}/ISteamApps/GetAppList/v2/"
    response = requests.get(url)
    games = response.json().get("applist", {}).get("apps", [])
    
    if search:
        return [g for g in games if search.lower() in g["name"].lower()]
    return games

def get_steam_game_details(app_id: int, pais_code: str = "CO") -> Dict[str, Any]:  # str = "COP"
    """Obtiene detalles completos de un juego, incluyendo precio en la moneda especificada.
    https://store.steampowered.com/api/appdetails/?appids=2623190
    https://store.steampowered.com/api/appdetails/?appids=2623190&cc=co&l=spanish
    {
      "name": "The Elder Scrolls IV: Oblivion Remastered",
      "price": "COL$ 198.900",
      "currency": "COP",
      "short_description": "Explora Cyrodiil como nunca con unos gráficos impresionantes y una jugabilidad mejorada en The Elder Scrolls IV: Oblivion™ Remastered.",
      "discount": 0,
      "release_date": "22 ABR 2025",
      "developers": [
        "Bethesda Game Studios",
        "Virtuos"
      ],
      "header_image": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2623190/a7cee9165bb1bfc092c390c5cff215ce0e381dfc/header.jpg?t=1745345472"
    }
    """
    params = {
        "appids": app_id,
        "cc": pais_code.lower(),  # Ej: "co" para colombia
        "l": "spanish"           # Idioma (opcional), english, spanish por defecto
    }
    response = requests.get(STEAM_STORE_BASE, params=params)
    data = response.json()
    
    if not data.get(str(app_id), {}).get("success"):
        return {"error": "Juego no encontrado o API falló"}
    
    game_data = data[str(app_id)]["data"]
    
    # Extrae información relevante
    return {
        "name": game_data.get("name"),
        "price": game_data.get("price_overview", {}).get("final_formatted", "N/A"),
        "currency": game_data.get("price_overview", {}).get("currency", "N/A"),
        "short_description": game_data.get("short_description"),
        "discount": game_data.get("price_overview", {}).get("discount_percent", 0),
        "release_date": game_data.get("release_date", {}).get("date"),
        "developers": game_data.get("developers", []),
        "header_image": game_data.get("header_image")
    }

def get_game_price(app_id: str, currency: str = "COP") -> dict:
    """Obtiene precio de un juego (requiere web scraping o API alternativa)."""
    # NOTA: Steam no expone precios directamente en su API. Usaremos SteamDB o scraping.
    return {"message": "Usar SteamDB o CheapShark para precios."}

# app/services/steam_service.py
from requests_html import HTMLSession

def get_steamdb_price(app_id: str, currency: str = "COP"):
    """
    ej:
    The Elder Scrolls IV: Oblivion Remastered
    https://steamdb.info/app/2623190/
    """
    session = HTMLSession()
    url = f"https://steamdb.info/app/{app_id}/"
    r = session.get(url)
    price = r.html.find(".table-prices td[data-cc=co]", first=True)
    return {"price": price.text if price else "No encontrado"}


'''
def get_game_full_details(app_id: int):
    steam_data = get_steam_game_details(app_id)
    steamdb_data = get_steamdb_price(app_id)
    return {**steam_data, "historical_low": steamdb_data.get("price")}

from functools import lru_cache

@lru_cache(maxsize=100)
def get_steam_game_details(app_id: int, currency: str = "COP"):
    # ... misma lógica
'''
