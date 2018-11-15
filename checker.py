from concurrent.futures import ThreadPoolExecutor
from typing import List, Iterable, Tuple
from urllib import request


def multi_fetch(urls: Iterable[str]) -> List[Tuple]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(fetch, urls)


async def fetch(url):
    try:
        result = request.urlopen(url)
        return result.getcode(), None
    except request.URLError as e:
        return '---', str(e)
    except Exception as e:
        return '???', str(e) or str(type(e))
