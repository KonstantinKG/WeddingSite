import os
import traceback

from flask_cors import CORS
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['POST'])
def add_data_to_google_sheets():
    try:
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        spreadsheet_id = 'base'
        values = [request.form.getlist('data')]
        body = {'values': values}

        result = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range='A1', valueInputOption='RAW', body=body).execute()
        return jsonify({"status": True})
    except Exception as e:
        print(e, traceback.format_exc())
        return jsonify({"status": False})


if __name__ == '__main__':
    app.run()
