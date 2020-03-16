import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_formatting as gsf

class Excel:

    def __init__(self, creds = 'creds.json', name = 'Sheets', worksheet = 'Январь'):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, scope)
        self.name_sheet = name
        self._client = gspread.authorize(credentials)
        self._sheet = self._client.open(name).sheet1

    def get_values(self, row, column):
        return self._sheet.cell(row, column).value

    def get_all_row(self, row):
        return self._sheet.row_values(row)

    def set_value(self, row, column, value):
        self._sheet.update_cell(row, column, value)

    def select_worksheet(self, name='Январь'):
        self._sheet = self._client.open(self.name_sheet).worksheet(name)

    def get_list_of_all_names_sheets(self):
        return self._client.open(self.name_sheet).worksheets()

    def set_color(self):
        fmt = gsf.cellFormat(
            textFormat=gsf.textFormat(
                bold=True, foregroundColor=gsf.color(112, 48, 160), fontSize=24)
        )
        gsf.format_cell_range(self._sheet, 'B1:B1', fmt)



doc = Excel()
doc.select_worksheet()
print(doc.get_values(9,10))
print(doc.get_list_of_all_names_sheets())