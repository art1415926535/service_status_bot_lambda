from concurrent.futures import ThreadPoolExecutor
from typing import List, Iterable, Tuple

import requests


def multi_fetch(urls: Iterable[str]) -> List[Tuple]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(fetch, urls)


def fetch(url):
    try:
        response = requests.get(url)
        return response.status_code, None
    except requests.RequestException as e:
        return '---', str(e)
    except Exception as e:
        return '???', str(e) or str(type(e))
