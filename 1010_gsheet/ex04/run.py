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

  values = [ [ 'hoge' ] ]
  body = { 'values' : values }

  # Call the Sheets API
  SPREADSHEET_ID = '1dbaI85LP1wxyuTcN2SBk3hkD-OO9-PNyjfBb0-ARnVY'
  RANGE_NAME = 'Sheet1!A2:E'
  value_input_option = 'USER_ENTERED'
  result = service.spreadsheets().values().update(
   spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
   valueInputOption=value_input_option, body=body).execute()
  print('{0} cells updated.'.format(result.get('updatedCells')));

if __name__ == '__main__':
  main()
