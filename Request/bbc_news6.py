import feedparser

# BBC Top Stories RSS URL
rss_url = "https://feeds.bbci.co.uk/news/rss.xml"

# Parse the feed
feed = feedparser.parse(rss_url)

print(f"--- Fetching: {feed.feed.title} ---\n")

# Loop through articles and print Title + Link
for entry in feed.entries:
    print(f"Title: {entry.title}")
    print(f"Link:  {entry.link}")
    print("-" * 40)