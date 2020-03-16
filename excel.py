import httplib2
from apiclient import  discovery
from oauth2client.service_account import ServiceAccountCredentials

class Excel:
    '''
    test = Excel()
    print(test.get_values('A4', 'G4'))
    test.set_values('E10', 'E10', title='Февраль', value=[['E']])
    print(test.find_sheet('Февраль'))
    test.set_color(0,2,0,2, 'Февраль', horizontal_alignment='LEFT')
    print(test.get_color('E10', 'Февраль'))
    test.copy_sheet()
    test.set_title()
    '''
    def __init__(self, CREDENTIALS_FILE='creds.json', spreadsheet_id='16HH4HYfXpmjBxnLpWM0ayiWWkHx-lKTxAQB7NPKqD18'):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        self._httpAuth = credentials.authorize(httplib2.Http())
        self._service = discovery.build('sheets', 'v4', http=self._httpAuth)
        self._spreadsheet_id = spreadsheet_id

    def get_values(self, start, end, title):
        values = self._service.spreadsheets().values().get(
            spreadsheetId=self._spreadsheet_id,
            range=f'{title}{start}:{end}',
            majorDimension='COLUMNS'
        ).execute()
        return values.get('values', [])

    def set_values(self, start, end, title, majorDimension = 'ROWS', value=''):
        self._service.spreadsheets().values().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"{title}!{start}:{end}",
                     "majorDimension": majorDimension,
                     "values": value,
                     }
                ]
            }
        ).execute()

    def find_sheet(self, title):
        sheet_meta = self._service.spreadsheets().get(spreadsheetId=self._spreadsheet_id).execute()
        sheets = sheet_meta.get('sheets', [])
        for id, sheet in enumerate(sheets):
            name_sheet = sheet.get("properties", {}).get("title", "Sheet1")
            if title == name_sheet:
                index = id
                return sheet.get("properties",{}).get("sheetId", {}) #index,

    def get_color(self, cell, title):
        sheet_meta = self._service.spreadsheets().get(spreadsheetId=self._spreadsheet_id, ranges=f'{title}!{cell}:{cell}',
                                                includeGridData=True).execute()
        sheets = sheet_meta['sheets']
        data = sheets[0]['data']
        row_data = data[0]['rowData']
        values = row_data[0]['values']
        user_entered_format = values[0]['userEnteredFormat']
        try:
            background_color = user_entered_format['backgroundColor']
        except:
            return {'red': 1.0, 'green': 1.0, 'blue': 1.0}
        return background_color

    #very bad
    def set_color(self, start_row:int, end_row, start_column:int, end_column, title='Январь', horizontal_alignment='CENTER', red=1.0, green=1.0, blue=1.0):
        self._service.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body = {
                "requests":
                    [
                        {
                            "repeatCell":
                                {
                                    "cell":
                                        {
                                            "userEnteredFormat":
                                                {
                                                    "horizontalAlignment": horizontal_alignment,
                                                    "backgroundColor": {
                                                        "red": str(red),
                                                        "green": str(green),
                                                        "blue": str(blue)
                                                    }
                                                }
                                        },
                                    "range":
                                        {
                                            "sheetId": str(self.find_sheet(title)),#january
                                            "startRowIndex": str(start_row+1),
                                            "endRowIndex": str(end_row),
                                            "startColumnIndex": str(start_column+1),
                                            "endColumnIndex": str(end_column)
                                        },
                                    "fields": "userEnteredFormat"
                                }},{
                            'updateBorders': {'range': {'sheetId': str(self.find_sheet(title)),
                                                        "startRowIndex": str(start_row+1),
                                                        "endRowIndex": str(end_row),
                                                        "startColumnIndex": str(start_column+1),
                                                        "endColumnIndex": str(end_column)},
                                              'bottom': {
                                                  # Задаем стиль для верхней границы
                                                  'style': 'SOLID',  # Сплошная линия
                                                  'width': 1,  # Шириной 1 пиксель
                                                  'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                                              # Черный цвет
                                              'top': {
                                                  # Задаем стиль для нижней границы
                                                  'style': 'SOLID',
                                                  'width': 1,
                                                  'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                                              'left': {  # Задаем стиль для левой границы
                                                  'style': 'SOLID',
                                                  'width': 1,
                                                  'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                                              'right': {
                                                  # Задаем стиль для правой границы
                                                  'style': 'SOLID',
                                                  'width': 1,
                                                  'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                                              'innerHorizontal': {
                                                  # Задаем стиль для внутренних горизонтальных линий
                                                  'style': 'SOLID',
                                                  'width': 1,
                                                  'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                                              'innerVertical': {
                                                  # Задаем стиль для внутренних вертикальных линий
                                                  'style': 'SOLID',
                                                  'width': 1,
                                                  'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}}
                        }
                        }
                    ]

            }
        ).execute()

    def copy_sheet(self, sheetId = 0):
        self._service.spreadsheets().sheets().copyTo(
            spreadsheetId = self._spreadsheet_id,
            sheetId = sheetId,
            body = {'destination_spreadsheet_id': self._spreadsheet_id}
        ).execute()
    #Не работает
    def set_title(self, sheetId=0):
        self._service.spreadsheets().sheets().rename(
            spreadsheetId = self._spreadsheet_id,
            sheetId = sheetId,
            body = {'title':'Test'})

test = Excel()
#print(test.__doc__)
#print(test.get_values('A4', 'G4'))
#test.set_values('E10', 'E10', title='Февраль', value=[['E']])
#print(test.find_sheet('Февраль'))
#test.set_color(0,2,0,2, 'Февраль', horizontal_alignment='LEFT')
#print(test.get_color('E11', 'Февраль'))
print(test.get_color('E26', 'Февраль'))
#test.copy_sheet()
#test.set_title()