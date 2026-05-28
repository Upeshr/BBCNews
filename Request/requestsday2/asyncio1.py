import asyncio
import aiohttp
import time

urls = ["https://httpbin.org/delay/2"]

async def fetch(url, session):
    async with session.get(url) as response:
        print(response.status)
        return await response.text()
    
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(url, session))

        results = await asyncio.gather(*tasks)

start = time.time()

asyncio.run(main())

end = time.time()

print(f"\nTotal: {end - start:.2f} Seconds")