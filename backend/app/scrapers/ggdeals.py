# app/scrapers/ggdeals.py
from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Optional

def make_soup(url: str) -> BeautifulSoup:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()  # Lanza error si hay problemas HTTP
    return BeautifulSoup(response.content, "html.parser")

def scrape_ggdeals_game(game_html: str) -> Dict[str, Optional[str]]:
    """Extrae datos de un solo juego (ya implementado por ti)"""
    soup = BeautifulSoup(game_html, 'html.parser')
    
    game_data = {
        'title': None,
        'url': None,
        'image_url': None,
        'game_pass': False,
        'genres': [],
        'release_date': None,
        'price': None,
        'original_price': None,
        'discount': None,
        'stores': [],
        'platforms': [],
        'game_id': None,
        'subscription_available': None
    }
    
    # Extraer ID del juego
    game_container = soup.find('div', class_='game-list-item')
    if game_container:
        game_data['game_id'] = game_container.get('data-container-game-id')
    
    # Extraer título y URL
    title_link = soup.find('a', class_='title-inner')
    if title_link:
        game_data['title'] = title_link.get_text(strip=True)
        game_data['url'] = title_link.get('href')
    
    # Extraer imagen (usando srcset como fallback)
    img_tag = soup.find('img', loading='lazy')
    if img_tag:
        game_data['image_url'] = img_tag.get('src') or img_tag.get('srcset', '').split()[0]
    
    # Verificar si está en Game Pass u otro servicio
    subscription_div = soup.find('div', class_='game-item-top-subscriptions')
    if subscription_div:
        game_data['game_pass'] = True
        game_data['subscription_available'] = subscription_div.get('data-original-title', '')
    
    # Extraer géneros
    genres_tag = soup.find('div', class_='genres-tag')
    if genres_tag:
        game_data['genres'] = [span.get_text(strip=True) 
                              for span in genres_tag.find_all('span', class_='value')]
    
    # Extraer fecha de lanzamiento
    date_tag = soup.find('div', class_='date-tag')
    if date_tag:
        game_data['release_date'] = date_tag.find('span', class_='value').get_text(strip=True)
    
    # Extraer información de precios
    price_wrapper = soup.find('div', class_='shop-price-wrapper')
    if price_wrapper:
        price = price_wrapper.find('span', class_='price-inner')
        if price:
            game_data['price'] = price.get_text(strip=True)
        
        discount = price_wrapper.find('span', class_='discount')
        if discount:
            game_data['discount'] = discount.get_text(strip=True)
        
        # Algunos juegos muestran el precio original tachado
        original_price = price_wrapper.find('span', class_='price-old')
        if original_price:
            game_data['original_price'] = original_price.get_text(strip=True)
    
    # Extraer información de tiendas
    store_wrapper = soup.find('div', class_='game-stores-wrapper')
    if store_wrapper:
        store_img = store_wrapper.find('img', class_='store-favicon')
        if store_img:
            game_data['stores'].append({
                'name': store_img.get('alt', '').strip(),
                'image': store_img.get('src', '')
            })
        
        store_name = store_wrapper.find('span', class_='game-store-name')
        if store_name:
            if game_data['stores']:
                game_data['stores'][0]['name'] = store_name.get_text(strip=True)
            else:
                game_data['stores'].append({
                    'name': store_name.get_text(strip=True),
                    'image': ''
                })
        
        more_stores = store_wrapper.find('span', class_='game-store-more')
        if more_stores:
            game_data['stores'].append({
                'name': more_stores.get_text(strip=True),
                'image': ''
            })
    
    # Extraer plataformas (método robusto)
    platforms = set()
    
    # Método 1: De data-original-title
    platforms_span = soup.find('span', class_='tag-icons')
    if platforms_span and 'data-original-title' in platforms_span.attrs:
        platforms_html = platforms_span['data-original-title']
        platforms_soup = BeautifulSoup(platforms_html, 'html.parser')
        platforms.update(span.get_text(strip=True) for span in platforms_soup.find_all('span'))
    
    # Método 2: De clases SVG (como respaldo)
    platform_icons = soup.find_all('span', class_='platform-link-icon')
    for icon in platform_icons:
        svg = icon.find('svg')
        if svg and 'class' in svg.attrs:
            platform_class = next((c for c in svg['class'] if c.startswith('svg-platform-')), None)
            if platform_class:
                platform_name = platform_class.replace('svg-platform-', '').replace('-', ' ').title()
                platforms.add(platform_name)
    
    game_data['platforms'] = list(platforms)
    
    return game_data

#def scrape_ggdeals_page(url: str) -> List[Dict[str, Optional[str]]]:
def scrape_ggdeals_list(url: str) -> List[Dict]:
    """Extrae todos los juegos de una página de GG.deals"""
    soup = make_soup(url)
    game_items = soup.find_all('div', class_='game-list-item')
    return [scrape_ggdeals_game(str(game)) for game in game_items]

def scrape_ggdeals_game_details(url: str) -> List[Dict]:
    """Extrae información de ofertas de un juego específico en GG.deals"""
    soup = make_soup(url)
    deals_container = soup.find_all('div', class_='game-deals-item')
    
    game_data_list = []
    
    for deal in deals_container:
        game_data = {
            'title': deal.find('a', class_='game-info-title').text.strip() if deal.find('a', class_='game-info-title') else None,
            'shop_name': deal.get('data-shop-name'),
            'current_price': deal.get('data-deal-value'),
            'original_price': deal.find('span', class_='price-old').text.strip() if deal.find('span', class_='price-old') else None,
            'discount': deal.find('span', class_='discount').text.strip() if deal.find('span', class_='discount') else None,
            'deal_status': deal.find('span', class_='best').text.strip() if deal.find('span', class_='best') else None,
            'drm': deal.find('svg')['title'] if deal.find('svg') and 'title' in deal.find('svg').attrs else None,
            'time_added': deal.find('time', class_='timeago-short')['datetime'] if deal.find('time', class_='timeago-short') else None,
            'expiry': deal.find('time', class_='timesince')['datetime'] if deal.find('time', class_='timesince') else None,
            'shop_link': deal.find('a', class_='shop-link')['href'] if deal.find('a', class_='shop-link') else None
        }
        game_data_list.append(game_data)
    
    game_title = game_data_list[0]['title'] if game_data_list else None
    
    return {
        #'game_title': soup.find('h1', class_='game-title').text.strip() if soup.find('h1', class_='game-title') else None,
        'game_title': game_title,
        'deals': game_data_list
    }
