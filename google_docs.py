# Description: This script creates a new Google Doc  

import os
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# SCOPE: drive.file (Recommended; Non-sensitive)
# See, edit, create, and delete only the specific Google Drive files you use with this app.	
# SCOPE: documents and drive (Sensitive)
# See, edit, create, and delete Google Docs documents and Drive files.
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]

def credentials():
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds

def delete_google_doc(document_id, creds=None):
    creds = creds or credentials()
    drive_service = build("drive", "v3", credentials=creds)
    body_value = {'trashed': True}
    response = drive_service.files().update(fileId=document_id, body=body_value).execute()

def build_requests(text, column_count = 1):
  requests = [
    {
      "insertText": {
        "location": {
          "index": 1
        },
        "text": text
      }
    },
    {
      "updateSectionStyle": {
        "sectionStyle": {
          "columnProperties": [
            {
              "paddingEnd": {
                "magnitude": 30,
                "unit": "PT"
              }
            },
            {
              "paddingEnd": {
                "magnitude": 30,
                "unit": "PT"
              }
            },
            {
              "paddingEnd": {
                "magnitude": 30,
                "unit": "PT"
              }
            }
          ]
        },
        "fields": "columnProperties",
        "range": {
          "startIndex": 0,
          "endIndex": column_count - 1
        }
      }
    }
  ]

  return requests

def batch_update(document_id, requests):
  creds = credentials()

  try:
    service = build("docs", "v1", credentials=creds)

    result = service.documents().batchUpdate(
      documentId=document_id, body={"requests": requests}
    ).execute()

  except HttpError as err:
    print(err)

def create_google_doc(doc_title):
  creds = credentials()

  try:
    service = build("docs", "v1", credentials=creds)

    document = service.documents().create(body={"title": doc_title}).execute()
    document_id = document.get("documentId")
    print(f"The title of the document is: {document.get('title')}  (Id: {document_id})")

    return document_id

  except HttpError as err:
    print(err)
    delete_google_doc(document_id, creds)

def main():
  document_id = create_google_doc([["Song 1", "Song 2", "Song 3"], ["Song 4", "Song 5", "Song 6"]])
  input("\nCheck file the press enter to delete")
  delete_google_doc(document_id)

if __name__ == "__main__":
  main()