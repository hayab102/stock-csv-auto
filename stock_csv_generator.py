import yfinance as yf
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# Google Sheets 認証
credentials_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
gc = gspread.authorize(credentials)

# スプレッドシートとワークシートを開く
spreadsheet = gc.open("stock_sheet")  # 適宜修正
sheet = spreadsheet.sheet1

# 株価データ取得
ticker = "7203.T"
df = yf.download(ticker, period="10d", interval="1d")
df.reset_index(inplace=True)

# ✅ Timestampを文字列に変換
df = df.astype(str)

# ✅ NaN のままではダメ。空文字に変換
df = df.fillna("")

# 2次元リストに変換（列名 + データ）
data = [df.columns.tolist()] + df.values.tolist()

# ✅ 書き込み（引数順が正しい）
sheet.update(values=data, range_name="A1")

print("✅ 完了: Google Sheets にデータを更新しました。")
