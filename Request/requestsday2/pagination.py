import requests

all_post = []
url = "https://jsonplaceholder.typicode.com/posts"

for page in range(1, 5):
    print(f"\n------Page {page}-------")

    response = requests.get(url + f"?_page={page}&_limit=5")
    data = response.json()
    for post in data:
        api = {"id": post["id"],
                "title": post["title"]}
        # all_post.append(post["id"])
        # all_post.append(post["title"])
        # print(post["id"], post["title"])
        all_post.append(api)
    print(all_post)