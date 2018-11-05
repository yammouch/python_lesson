from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
#SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  store = file.Storage('token.json')
  creds = store.get()
  if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
  service = build('sheets', 'v4', http=creds.authorize(Http()))

  title = 'title_hoge'
  requests = []
  requests.append({
    'updateSpreadsheetProperties': {
      'properties': {
        'title': title
      },
      'fields': 'title'
    }
  })
  body = {
    'requests': requests
  }

  # Call the Sheets API
  SPREADSHEET_ID = '1dbaI85LP1wxyuTcN2SBk3hkD-OO9-PNyjfBb0-ARnVY'
  RANGE_NAME = 'Sheet1!A2:E'
  value_input_option = 'USER_ENTERED'
  response = service.spreadsheets().batchUpdate(
   spreadsheetId=SPREADSHEET_ID, body=body).execute()
  print(response)

if __name__ == '__main__':
  main()
