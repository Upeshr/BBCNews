import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.com/news"

# Added a User-Agent so the BBC server doesn't instantly block the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # BBC organizes their main articles inside 'promo' or 'anchor' containers
    # We find all links that have a data-testid containing "outer-heading" or "link"
    links = soup.find_all('a', href=True)
    
    seen_links = set()
    
    print("--- Scraping BBC News Homepage ---\n")
    
    for link in links:
        href = link['href']
        title = link.get_text(strip=True)
        
        # Filter for actual news articles and ensure we have a title text
        if "/news/articles/" in href and title and href not in seen_links:
            seen_links.add(href)
            
            # Format relative URLs to full URLs
            full_url = href if href.startswith("https") else f"https://www.bbc.com{href}"
            
            print(f"Title: {title}")
            print(f"Link:  {full_url}")
            print("-" * 40)
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")