import asyncio
import aiohttp

URLS = [
    "https://httpbin.org/get",
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2"
]

async def fetch(url, session):
    async with session.get(url) as response:
        data = await response.text()
        print(f"{url} -> {response.status}")


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in URLS:
            tasks.append(fetch(url, session))
        results = await asyncio.gather(*tasks)

asyncio.run(main()) 