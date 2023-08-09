import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SCOPE_WRITE = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['POST'])
def add_data_to_google_sheets():
    try:
        data = request.get_json()

        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)

        spreadsheet_id = "1TAI7mPmJcy2DyeXu7A4kiUhJLdG453pzf0-BEs-aypw"

        body = {
            "values": [[data["username"], data["value"]]]
        }

        response = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range='Sheet1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        print(response)
        return jsonify({"status": True})
    except Exception as e:
        print(e, traceback.format_exc())
        return jsonify({"status": False})


if __name__ == '__main__':
    app.run()
