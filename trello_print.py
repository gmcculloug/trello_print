# This script lists the Trello lists for a board and the cards in each list.
# 
# Usage: python trello_print.py <column_name>
# Example: python trello_print.py Set List 1
# 
# Environment variables:
#   - TRELLO_DEVELOPER_PUBLIC_KEY: Trello developer public key
#   - TRELLO_MEMBER_TOKEN: Trello member token
#   - TRELLO_BOARD_ID: Trello board ID

import sys
import datetime
from trello_api import get_set_list, print_set_lists
from google_docs import create_google_doc, build_requests, batch_update

def songs(set_lists):
  songs = ""
  for lst in set_lists:
    songs += ("\n".join(str(x) for x in lst))
    songs += "\n\n"

  return songs

def add_set_list_to_doc(document_id, set_lists):
    song_text = songs(set_lists)
    requests = build_requests(song_text, len(set_lists))
    batch_update(document_id, requests)

def main():
  # Get the Trello column name from the command arguments
  if len(sys.argv) < 2:
    print("Usage: python trello_list.py <column_name>")
    exit()

  column_name = " ".join(sys.argv[1:])
  print(f"Column Name: {column_name}\n")

  set_lists = get_set_list(column_name)
  print_set_lists(set_lists)

  # Ask user if they want to create a Google Doc
  create_doc = input("\nDo you want to create a Google Doc?  [Default: n]: ") or "n"
  # create_doc = 'n'
  if create_doc.lower() == "y":
    # Create document title with date and time in the 12 hour format: YYYY-MM-DD_HH-MM
    doc_title = datetime.datetime.now().strftime("%Y-%m-%d_%I-%M")
    document_id = create_google_doc(doc_title)
    add_set_list_to_doc(document_id, set_lists)

if __name__ == "__main__":
  main()