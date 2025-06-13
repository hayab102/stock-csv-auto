import yfinance as yf
import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# 認証情報の読み込み（GitHub Secrets から）
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# データ取得
ticker = "AAPL"
df = yf.download(ticker, period="10d", interval="1d")
df.reset_index(inplace=True)
df = df.fillna("")        # NaN を空文字に
df = df.astype(str)       # すべて文字列に変換

# スプレッドシートの準備
spreadsheet = client.open("stock_sheet")  # スプレッドシート名
sheet = spreadsheet.sheet1                # 最初のワークシートを選択

# シートへアップロード
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ stock.csv saved and uploaded to Google Sheets.")
