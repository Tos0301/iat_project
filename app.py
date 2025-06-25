from flask import Flask, render_template, request, jsonify
import os, json, base64
import datetime
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# ----------------------------
# Google Sheets API認証（環境変数から）
# ----------------------------
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Renderに設定したBase64文字列を復号
encoded = os.environ.get('ENCODED_CREDENTIALS')
decoded_json = base64.b64decode(encoded).decode('utf-8')
creds_dict = json.loads(decoded_json)

# 認証情報を使ってgspread認証
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
gc = gspread.authorize(creds)

# ご自身のスプレッドシートIDに置き換えてください
SHEET_ID = '1Lk70YIiaIg7BM4zKHShf5ziWpswwvMGw6yKsDp-cpbk'
worksheet = gc.open_by_key(SHEET_ID).sheet1

# ----------------------------
# Flaskルーティング
# ----------------------------

@app.route('/')
def index():
    return render_template('iat.html')

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    row = [
        data.get('participant_id'),
        data.get('block'),
        data.get('stimulus'),
        data.get('response'),
        data.get('correct'),
        data.get('reaction_time'),
        datetime.datetime.now().isoformat()
    ]
    worksheet.append_row(row)
    return jsonify({'status': 'success'})

# ----------------------------
# アプリ実行（Renderおよびローカル用）
# ----------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render環境ではPORTが与えられる
    app.run(host='0.0.0.0', port=port, debug=True)
