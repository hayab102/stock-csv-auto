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

# スプレッドシートに接続
spreadsheet = gc.open("stock_sheet")  # 適宜変更
sheet = spreadsheet.sheet1

# 株価データを取得
ticker = "7203.T"
df = yf.download(ticker, period="10d", interval="1d")

# インデックスを列に戻す（Date を含める）
df.reset_index(inplace=True)

# NaN → 空文字, すべて文字列へ
df = df.fillna("").astype(str)

# ✅ 列名を文字列として扱い、空文字を除外
df.columns = [str(col).strip() if str(col).strip() != "" else "Unnamed" for col in df.columns]

# Google Sheets に書き込む形式に
data = [df.columns.tolist()] + df.values.tolist()

# 書き込み（range → values の順）
sheet.update(range_name="A1", values=data)

print("✅ 完了しました！Google Sheets にデータが正常に書き込まれました。")
