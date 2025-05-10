# app/api/endpoints/games.py  
from fastapi import APIRouter  
from app.services.steam_service import get_steam_game_list, get_steamdb_price  
from app.services.nuuvem_service import search_nuuvem  

router = APIRouter(prefix="/games", tags=["Games"])  

@router.get("/search")  
def search_all_stores(game_name: str):
    """
    http://localhost:8000/games/search?game_name=cyberpunk
    {  
      "steam": [{"appid": 1091500, "name": "Cyberpunk 2077"}],  
      "nuuvem": [{"name": "Cyberpunk 2077", "url": "/item/cyberpunk-2077"}]  
    }  
    """
    return {  
        "steam": get_steam_game_list(game_name),  
        "nuuvem": search_nuuvem(game_name)  
    }  

@router.get("/price/{store}/{game_id}")  
def get_game_price(store: str, game_id: str):
    """
    curl "http://localhost:8000/games/price/nuuvem/item/cyberpunk-2077"
    {"price": "$120.000 COP"}  
    """
    if store == "steam":  
        return get_steamdb_price(game_id)  
    elif store == "nuuvem":  
        return get_nuuvem_price(game_id)  
    return {"error": "Tienda no soportada"}  