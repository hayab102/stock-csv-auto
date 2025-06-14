import yfinance as yf
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# Google Sheets認証
credentials_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
gc = gspread.authorize(credentials)

# スプレッドシートとワークシート名
spreadsheet = gc.open("stock_sheet")  # ←シート名変更していたらここも修正
sheet = spreadsheet.sheet1

# 銘柄とデータ取得
ticker = "7203.T"
df = yf.download(ticker, period="10d", interval="1d")
df.reset_index(inplace=True)

# データ内のNaNを空文字に変換（Google Sheetsエラー回避）
df = df.fillna("")

# ヘッダー付きの2次元リストに変換
data = [df.columns.tolist()] + df.values.tolist()

# A1から書き込み
sheet.update(values=data, range_name="A1")

print("✅ stock.csv successfully updated to Google Sheets.")
