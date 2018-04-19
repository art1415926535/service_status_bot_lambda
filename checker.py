from typing import List, Iterable, Tuple, Optional

import aiohttp
import async_timeout
import asyncio


def multi_fetch(urls: Iterable[str]) -> List[Tuple]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    requests = [asyncio.ensure_future(fetch(url))
                for url in urls]
    responses = loop.run_until_complete(asyncio.gather(*requests))
    loop.close()
    return list(zip(*responses))


async def fetch(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(10):
                async with session.get(url) as response:
                    return response.status, None
    except aiohttp.ClientConnectorError as e:
        return '---', str(e)
    except Exception as e:
        return '???', str(e) or str(type(e))
