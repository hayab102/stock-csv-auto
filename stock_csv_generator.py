import yfinance as yf
import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# Google認証
credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

# 株データ取得
ticker = "AAPL"
df = yf.download(ticker, period="10d", interval="1d")

# データ整形
df.reset_index(inplace=True)
df.fillna("", inplace=True)       # 欠損値（NaN）を空文字に
df = df.astype(str)               # 全部文字列に変換（gspreadが通る形式）

# シート更新
sheet = client.open("stock_sheet").sheet1  # シート名に注意
sheet.clear()  # 既存データを削除
sheet.update([df.columns.tolist()] + df.values.tolist())

print("✅ Googleスプレッドシートにアップロード完了")
