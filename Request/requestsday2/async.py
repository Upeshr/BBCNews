import requests
import time

urls =["https://httpbin.org/delay/2"] * 10

start = time.time()

for url in urls:
    response = requests.get(url)
    print(response.status_code)

end = time.time()
print(f"\nTotal time: {end - start:.2f} Seconds")