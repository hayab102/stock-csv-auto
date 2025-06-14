import yfinance as yf
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# 認証
credentials_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
gc = gspread.authorize(credentials)

# スプレッドシート
spreadsheet = gc.open("stock_sheet")  # 適宜置き換え
sheet = spreadsheet.sheet1

# 株価データ取得
ticker = "7203.T"
df = yf.download(ticker, period="10d", interval="1d")
df.reset_index(inplace=True)

# ✅ 空白列名があると API エラー、強制的に埋める
df.columns = [col if col != "" else "Unnamed" for col in df.columns]

# ✅ 全データを文字列化
df = df.astype(str)

# ✅ NaN を空文字に
df = df.fillna("")

# ✅ シートに書き込み（ヘッダー + 本体）
data = [df.columns.tolist()] + df.values.tolist()
sheet.update(range_name="A1", values=data)

print("✅ 完了: データを正常に更新しました。")
