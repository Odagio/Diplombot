import apiclient.discovery
import httplib2 
import settings
from oauth2client.service_account import ServiceAccountCredentials	

CREDENTIALS_FILE = 'credentials.json'  # Имя файла с закрытым ключом, вы должны подставить свое
spreadsheet_id = settings.SPREAD_SHEET_ID
# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

values = service.spreadsheets().values().batchUpdate(
    spreadsheetId = spreadsheet_id, body = 
    {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "B2:C3",
         "majorDimension": "ROWS",     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
         "values": [["This is B2", "This is C2"], ["This is B3", "This is C3"]]},

        {"range": "D5:E6",
         "majorDimension": "COLUMNS",  # сначала заполнять столбцы, затем ряды (т.е. самые внутренние списки в values - это столбцы)
         "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
    ]
}).execute()
