from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json
#gspread
# keys
CREDENTIALS_FILE = 'creds.json'

# id table
spreadsheet_id = '16HH4HYfXpmjBxnLpWM0ayiWWkHx-lKTxAQB7NPKqD18'

# auth
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())

# select spreadsheet
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

# read data
start = 'A4'
end = 'G4'

sheet_meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges='A4:A4', includeGridData = True).execute()
#with open('tests.json', 'w') as file:
#    json.dump(sheet_meta, file)
sheets = sheet_meta.get('sheets', {})
data = sheets[0].get('data', {})
row_data = data[0].get('rowData', {})
values = row_data[0].get('values', {})
user_entered_format = values[0].get('userEnteredFormat', {})
print(user_entered_format['backgroundColor'])
print(type(sheet_meta.get('sheets', {})))

'''values = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"{start}:{end}",
             "majorDimension": "ROWS",
             "values": [[1, 2, 9, 4, 5, 6, 7]]}
	]
    }
).execute()'''