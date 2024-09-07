import requests
from bs4 import BeautifulSoup

# The url to scrape
url = 'https://weather.com'

# Store the html in r
r = requests.get(url)

print(r.content[:100])

# Create soup object with the type of parser (html) and the content to be parsed
soup = BeautifulSoup(r.content, 'html.parser')

