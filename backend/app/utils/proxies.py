# app/utils/proxies.py
import random

PROXY_LIST = [
    "http://45.177.109.241:999",
    "http://45.175.239.85:999",
    "http://190.61.88.147:8080",
    # Añade más proxies gratuitos de https://free-proxy-list.net/
]

def get_random_proxy():
    return {"http": random.choice(PROXY_LIST)}