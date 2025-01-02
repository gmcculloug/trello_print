import requests
import os

# Load the Trello API key and token from environment variables
TRELLO_KEY = os.getenv("TRELLO_DEVELOPER_PUBLIC_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_MEMBER_TOKEN")
# Load trello board ID from environment variable
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")

# Check if the TRELLO_DEVELOPER_PUBLIC_KEY environment variable is set
if not TRELLO_KEY:
  print("Please set the TRELLO_DEVELOPER_PUBLIC_KEY environment variable")
  exit()

# Check if the TRELLO_MEMBER_TOKEN environment variable is set
if not TRELLO_TOKEN:
  print("Please set the TRELLO_MEMBER_TOKEN environment variable")
  exit()

# Check if the TRELLO_BOARD_ID environment variable is set
if not TRELLO_BOARD_ID:
  print("Please set the TRELLO_BOARD_ID environment variable")
  exit()

def trello_api_request(url):
  query = {
    "key": TRELLO_KEY,
    "token": TRELLO_TOKEN
  }
  response = requests.get(url, params=query)
  return response.json()

def get_set_list(column_name):
  result = []

  # Get the Trello lists for the board
  lists = trello_api_request(f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists")

  for lst in lists:
    # Check if the list name contains the column name
    if column_name.lower() not in lst["name"].lower():
      continue

    # Append the list name to a string
    result.append([lst['name']])
    list_names = result[-1]

    # Get the cards in the list 
    cards = trello_api_request(f"https://api.trello.com/1/lists/{lst['id']}/cards")

    for card in cards:
      # Append the card name to the string
      list_names.append(card['name'])

  return result

def print_set_lists(set_lists):
  for lst in set_lists:
    print(lst[0])
    for song in lst[1:]:
      print(f"  - {song}")
