import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from prettytable import PrettyTable

# Provide the URL of the page you want to scrape
URL = 'https://htmx.org/essays/'
# Provide the CSS selector for the elements you want to scrape
SELECTOR = 'li > a'


# Function to handle the elements
def get_dated_links(link_tag):
    link_url = link_tag.get('href')
    link_response = requests.get(link_url)
    link_html = link_response.text
    link_soup = BeautifulSoup(link_html, 'html.parser')
    
    time_tag = link_soup.find('time')
    if time_tag:
        return [time_tag.text, link_tag.text, link_url]
    else:
        return ["", link_tag.text, link_url]


# Fetch the main page and parse it
page_response = requests.get(URL)
page_html = page_response.text
page_soup = BeautifulSoup(page_html, 'html.parser')

# Handle the elements concurrently
elements = page_soup.select(SELECTOR)
with ThreadPoolExecutor() as executor:
    results = executor.map(get_dated_links, elements)

# Print out in a table

table = PrettyTable()
table.field_names = ["Date", "Text", "URL"]
table.align["Date"] = "l"
table.align["Text"] = "l"
table.align["URL"] = "l"

for result in results:
    table.add_row(result)
print(table)
