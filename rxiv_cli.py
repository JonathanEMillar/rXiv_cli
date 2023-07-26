import requests
import json
import webbrowser 
import time
from urllib.parse import quote_plus, quote

API_URL = "https://api.biorxiv.org/details"

def medrxiv_search(search_term, server, days):
  
  search_term = "{%s}" % quote_plus(search_term) 

  server = quote(server)

  days = quote(days)

  url = f"{API_URL}/{server}/title/{days}d?query={search_term}"

  print(url)

  headers = {"Accept": "application/json"}

  try:
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
      print("Error accessing API:", response.status_code)
      return None

  except Exception as e:
    print("Error making API request:", e)  
    return None

  data = json.loads(response.content)

  if len(data['collection']) == 0:
    print("No results found")
    return None

  return data["collection"]


def open_in_browser(article, server):

  if article is None:
    return

  doi = article["doi"]
  url = f"https://www.{server}.org/content/{doi}"
    
  time.sleep(1)

  try:
    webbrowser.open(url)
  except Exception as e:
    print("Error opening browser:", e)


if __name__ == "__main__":

  term = input("Enter search term: ")
  server = input("Enter server: ")
  days = input("Enter number of days to search: ")
  results = medrxiv_search(term, server, days)

  print("Results:")

  for i, result in enumerate(results):
    title = result["title"]  
    date = result["date"]
    first_author = result["authors"].split(", ", 1)[0]
    first_author = first_author.title()

    print(f"{i+1}. {first_author}. {title}. {date}")

  index = int(input("\nEnter article number to open in browser: "))
  article = results[index-1]

  open_in_browser(article, server)