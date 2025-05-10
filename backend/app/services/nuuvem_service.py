# app/services/nuuvem_service.py  
from requests_html import HTMLSession  

session = HTMLSession()  

def search_nuuvem(game_name: str) -> list:  
    """Busca juegos en Nuuvem y devuelve nombres y URLs."""  
    url = f"https://www.nuuvem.com/search/{game_name}"  
    try:  
        r = session.get(url)  
        games = r.html.find(".product-card--grid")  
        results = []  
        for game in games[:5]:  # Limita a 5 resultados  
            title = game.find(".product-title", first=True).text  
            link = game.find("a", first=True).attrs["href"]  
            results.append({"name": title, "url": link})  
        return results  
    except Exception as e:  
        return {"error": str(e)}  

def get_nuuvem_price(game_url: str) -> dict:  
    """Obtiene precio de un juego específico en Nuuvem."""  
    try:  
        r = session.get(game_url)  
        price = r.html.find(".product-price--val", first=True).text  
        return {"price": price.strip()}  
    except Exception as e:  
        return {"error": str(e)}  