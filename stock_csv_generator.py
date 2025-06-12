import yfinance as yf
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# ---------- 設定 ----------
TICKER = "AAPL"                         # 任意のティッカー
SPREADSHEET_NAME = "株価シート"       # スプレッドシート名
CSV_FILENAME = "stock.csv"             # 保存ファイル名
# ---------------------------

# データ取得（10日分）
df = yf.download(TICKER, period="10d", interval="1d")
df.reset_index(inplace=True)  # 日付を列に
df = df.astype(str)           # 文字列変換（gspread対策）

# CSV保存
df.to_csv(CSV_FILENAME, index=False)
print(f"✅ {CSV_FILENAME} saved.")

# Google認証
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# スプレッドシート操作
spreadsheet = client.open(SPREADSHEET_NAME)
worksheet = spreadsheet.sheet1

# スプレッドシート更新
header = df.columns.tolist()
rows = df.values.tolist()
worksheet.update([header] + rows)

print("✅ スプレッドシート更新完了。")


