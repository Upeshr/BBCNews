import requests

# This API gives us a list of fake "leads" (Users)
url = "https://jsonplaceholder.typicode.com/users"

print("Fetching data from the public API...")

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Success! Found {len(data)} people.")
    print("-" * 30)
    
    for user in data:
        name = user['name']
        email = user['email']
        company = user['company']['name']
        print(f"Name: {name} | Email: {email} | Company: {company}")
else:
    print(f"Failed with code: {response.status_code}")