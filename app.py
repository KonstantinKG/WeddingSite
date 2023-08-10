import json
import traceback

from flask import Flask, request
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build

from helpers.logger import Logger

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SCOPE_WRITE = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

with open("config.json", 'r', encoding='utf-8') as file:
    config = json.loads(file.read())

logger = Logger().get_logger(name=config["source"])

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['POST'])
def add_data_to_google_sheets():
    try:
        data = request.get_json()
        logger.info(f"Writing info to excel file: {data['username']} { data['value']}")

        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)

        spreadsheet_id = "1TAI7mPmJcy2DyeXu7A4kiUhJLdG453pzf0-BEs-aypw"

        body = {
            "values": [[data["username"], data["value"]]]
        }

        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range='Sheet1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        return app.response_class(status=200)
    except Exception as e:
        logger.error(f"Failed to write data to excel error occurred {e}\nTRACEBACK {traceback.format_exc()}")
        return app.response_class(status=500)


if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'])
