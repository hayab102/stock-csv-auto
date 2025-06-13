import yfinance as yf
import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# 認証
credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

# データ取得
ticker = "AAPL"
df = yf.download(ticker, period="10d", interval="1d")

# データ加工
df.reset_index(inplace=True)
df = df.fillna("")       # NaNを空文字に置換
df = df.astype(str)      # すべて文字列化（gspreadが必要とする形式）

# スプレッドシートへ
sheet = client.open("stock_sheet").sheet1
sheet.clear()  # 一度全部消す（これ重要）
data = [df.columns.tolist()] + df.values.tolist()
sheet.update("A1", data)  # ← 書き出し開始位置を指定（必須）

print("✅ Google Sheets へアップロード完了")
