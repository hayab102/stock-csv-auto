import yfinance as yf
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# 株価データ取得
ticker = "AAPL"  # 必要なら他に変更
df = yf.download(ticker, period="10d", interval="1d")

# CSVに保存
df.to_csv("stock.csv")
print("✅ stock.csv saved.")

# Google Sheets に接続（GitHub Secretsから読み込む）
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("stock_sheet").sheet1  # シート名注意

# 日付を含む形式でアップロード
df = df.reset_index().astype(str)
sheet.update([df.columns.values.tolist()] + df.values.tolist())
