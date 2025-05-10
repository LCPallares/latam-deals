# app/main.py
from fastapi import FastAPI
from app.api.endpoints.steam import router as steam_router
from app.api.endpoints.games import router as games_router
from app.api.endpoints.ggdeals import router as ggdeals_router

app = FastAPI()
app.include_router(steam_router)  # ¡Endpoint disponible en /steam/games!
app.include_router(games_router)
app.include_router(ggdeals_router)  # Ahora disponible en /ggdeals/games

@app.get("/")
def root():
    return {"message": "API Latam Deals"}
