import yfinance as yf
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------
# ▼ 設定
ticker = "AAPL"  # 任意のティッカーに変更可
spreadsheet_name = "株価シート"  # 既に作成・共有済みのスプレッドシート名
csv_filename = "stock.csv"
# -------------------------------

# ▼ データ取得（10日間）
df = yf.download(ticker, period='10d', interval='1d')
df.reset_index(inplace=True)              # Date列をインデックスから戻す
df = df.astype(str)                       # すべて文字列に変換（gspread対応）

# ▼ CSV保存
df.to_csv(csv_filename, index=False)
print(f"✅ {csv_filename} saved.")

# ▼ Google Sheets 認証
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])  # GitHub Secretsに登録したJSON文字列
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# ▼ スプレッドシートへ反映
try:
    spreadsheet = client.open(spreadsheet_name)
    worksheet = spreadsheet.sheet1
    header = df.columns.tolist()
    values = df.values.tolist()
    worksheet.update([header] + values)
    print("✅ スプレッドシートに反映完了")
except gspread.exceptions.SpreadsheetNotFound:
    print("❌ スプレッドシートが見つかりません。名前や共有設定を確認してください。")
