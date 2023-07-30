### rXiv CLI

This is a command line tool for searching and retrieving preprint papers from bioRxiv and medRxiv servers.

#### Usage

To use the tool, run:

```
python rxiv_cli.py
```

You will be prompted to enter:

-    The server to search - either biorxiv or medrxiv

-    Number of days back to search

-    Search term

The script will retrieve papers from the specified server in the given date range, search the titles and abstracts for the search term, and print out matches.

You can then enter the number of a paper to open its page in your default web browser.

#### Requirements

The script requires the following Python packages:

requests, json, webbrowser, datetime, urllib

Install any missing packages before running the script

```Shell
pip install -r requirements.txtl 

#### Output

The script prints out the matched papers with the title, first author, date, and DOI.

It then allows opening the paper's page in a web browser by entering its number.

#### Notes

-    The search is limited to 3 days back due to API restrictions

-    Invalid inputs will print error messages

-    No matches found will exit the program

#### Credits

API provided by bioRxiv/medRxiv: <https://api.biorxiv.org/>
