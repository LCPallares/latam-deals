import requests
import random
import time
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# 1. Proxies Gratuitos
PROXY_LIST_FREE = [
    "http://45.177.109.241:999",
    "http://45.175.239.85:999",
    "http://190.61.88.147:8080"
]

# 2. Servicios de Scraping (Configura en Render)
SCRAPING_SERVICES = {
    'scrapingbee': {
        'url': 'https://app.scrapingbee.com/api/v1/',
        'env_key': 'SCRAPINGBEE_API_KEY'  # Nombre de variable de entorno
    }
}

def get_headers() -> Dict[str, str]:
    """Genera headers realistas para las peticiones"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://gg.deals/'
    }

def make_web_request(url: str, max_retries: int = 3) -> Optional[requests.Response]:
    """
    Sistema inteligente de peticiones con:
    - Intentos directos
    - Proxies gratuitos
    - Servicios profesionales (ScrapingBee)
    """
    strategies = [
        {'method': 'direct', 'timeout': 10},
        {'method': 'proxy_free', 'timeout': 15},
        {'method': 'scraping_service', 'service': 'scrapingbee', 'timeout': 20}
    ]

    for attempt in range(max_retries):
        strategy = strategies[min(attempt, len(strategies)-1)]
        
        try:
            logger.info(f"Attempt {attempt+1} - Strategy: {strategy['method'].upper()}")

            if strategy['method'] == 'direct':
                response = requests.get(
                    url,
                    headers=get_headers(),
                    timeout=strategy['timeout']
                )
            elif strategy['method'] == 'proxy_free':
                proxy = {"http": random.choice(PROXY_LIST_FREE)}
                response = requests.get(
                    url,
                    headers=get_headers(),
                    proxies=proxy,
                    timeout=strategy['timeout']
                )
            elif strategy['method'] == 'scraping_service':
                service_config = SCRAPING_SERVICES[strategy['service']]
                api_key = os.getenv(service_config['env_key'])
                if not api_key:
                    raise ValueError(f"API key missing for {strategy['service']}")
                
                params = {
                    'url': url,
                    'api_key': api_key,
                    'render_js': 'false'
                }
                response = requests.get(
                    service_config['url'],
                    params=params,
                    timeout=strategy['timeout']
                )

            response.raise_for_status()
            return response

        except Exception as e:
            logger.warning(f"Strategy {strategy['method']} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    
    return None