import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import unittest
from excel import Excel

class TestExcel(unittest.TestCase):
    def setUp(self):
        self.excel = Excel()

    def test_get_values_cell(self):
        self.assertEqual(self.excel.get_values(start='G4', end='G4', title='Февраль'), [['09.00 -- 18.00']])

    def test_get_values_column(self):
        self.assertEqual(self.excel.get_values(start='A4', end='G4', title='Февраль'),
                         [[], ['Куприянова Анастасия'], ['499'], ['SMR'], ['09.00 -- 18.00'], ['09.00 -- 18.00'], ['09.00 -- 18.00']])

