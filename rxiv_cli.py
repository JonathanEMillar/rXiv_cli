import requests
import json
import webbrowser 
import time
import os
import csv
from datetime import datetime, timedelta
from urllib.parse import quote_plus, quote
from concurrent.futures import ThreadPoolExecutor


API_URL = "https://api.biorxiv.org/details"
VALID_SERVERS = ["biorxiv", "medrxiv"]


def get_input_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input, please enter an integer.")


def get_input_server(prompt):
    while True:
        value = input(prompt)
        if value in VALID_SERVERS:
            return value
        else:
            print("Invalid server. Please enter either 'biorxiv' or 'medrxiv'.")


def rxiv_retrieval(server, days):
  """
  Retrieves papers from the given server from the last specified number of days.
  
  Parameters:
  server (str): The name of the server to retrieve papers from.
  days (str): The number of days back to search for papers.

  Returns:
  list: A list of papers if any are found, None otherwise.
  """

  server = quote(server)

  days = int(days)
  if days > 3:
    print("Cannot search back this far")
    return None

  today = datetime.now()

  date_in_past = today - timedelta(days=days)

  date_in_past = date_in_past.date()

  today_fmt = today.strftime("%Y-%m-%d")

  date_in_past_fmt = date_in_past.strftime("%Y-%m-%d") 

  url = f"{API_URL}/{server}/{date_in_past}/{today_fmt}"

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


def rxiv_search(results, search_term):
  """
  Search for a term within the titles and abstracts of a collection of papers.

  Parameters:
  results (list): The collection of papers to search through.
  search_term (str): The term to search for.

  Returns:
  list: A list of papers that contain the search term.
  """
  matches = []
  search_term = search_term.lower()
  
  for result in results:
    title = result["title"].lower()
    abstract = result["abstract"].lower()
    
    if search_term in title or search_term in abstract:
      matches.append(result)

  return matches


def print_matches(matches):
  """
  Prints the title, first author, publication date, and the DOI of the papers.
  
  Parameters:
  matches (list): The list of papers to print.
  """

  for i, result in enumerate(matches):
    
    authors = result["authors"].split(", ")
    first_author = authors[0].split(" ")[-1]
    
    title = result["title"]
    date = result["date"]
    doi = result["doi"]
    
    print(f"{i+1}. {first_author} - {title} - {date} - {doi}")


def open_paper(matches):
  """
  Open the DOI URL of a paper in a web browser.

  Parameters:
  matches (list): The collection of papers that the paper is part of.
  """
  while True:
    selection = input("Enter number to open paper or 'q' to quit: ")

    if selection.lower() == 'q':
      break
    
    try:
      index = int(selection) - 1
      doi = matches[index]["doi"]
      url = f"https://doi.org/{doi}"
      webbrowser.open(url)
    except (IndexError, ValueError):
      print("Invalid input. Please enter a valid number or 'q' to quit.")


if __name__ == "__main__":
    server = get_input_server("Enter server: ")
    days = get_input_integer("Enter number of days back to search: ")
    search_term = input("Enter search term: ")

    if days <= 0:
        print("Number of days should be a positive integer.")
        sys.exit(1)

    results = rxiv_retrieval(server, days)
    if results is None:
        print("No results found. Exiting the program.")
        sys.exit(1)
  
    matches = rxiv_search(results, search_term)

    matches_number = len(matches)

    print(f"There were {matches_number} results matching {search_term}")

    print_matches(matches)

    open_paper(matches)

