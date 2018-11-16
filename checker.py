from concurrent.futures import ThreadPoolExecutor
from typing import List, Iterable, Tuple, Union
import os

import requests


timeout = int(os.environ.get('timeout', 3))


def get_status_codes(urls: Iterable[str]) -> List[Tuple]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(fetch_code, urls)


def fetch_code(url: str) -> Tuple[Union[str, int], Union[str, None]]:
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code, None
    except requests.Timeout:
        return 504, None
    except requests.RequestException as e:
        return '->x', str(e)
    except Exception as e:
        return '???', str(type(e))
