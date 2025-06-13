import yfinance as yf
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# 対象の銘柄（ticker）を指定
ticker = 'AAPL'

# データ取得
df = yf.download(ticker, period='10d', interval='1d')
df.reset_index(inplace=True)
df = df.astype(str)  # Google Sheetsへアップロードするため文字列化

# CSVファイルとして保存（オプション）
df.to_csv("stock.csv", index=False)
print("✅ stock.csv saved.")

# Google Sheets に接続
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# スプレッドシートに接続・アップロード
spreadsheet = client.open("stock_sheet")  # スプレッドシート名を正確に
worksheet = spreadsheet.sheet1  # 最初のシートを対象に

worksheet.update([df.columns.values.tolist()] + df.values.tolist())
print("✅ Google Spreadsheet updated.")
