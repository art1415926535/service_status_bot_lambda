from concurrent.futures import ThreadPoolExecutor
from typing import List, Iterable, Tuple

import requests


def get_status_codes(urls: Iterable[str]) -> List[Tuple]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(fetch_code, urls)


def fetch_code(url):
    try:
        response = requests.get(url)
        return response.status_code, None
    except requests.RequestException as e:
        return '---', str(e)
    except Exception as e:
        return '???', str(e) or str(type(e))
