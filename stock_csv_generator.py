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

# ✅ Timestamp列が混じるので、Indexをリセット
df.reset_index(inplace=True)

# ✅ すべてを「文字列化」かつ NaN を空文字に
df = df.fillna("").astype(str)

# ✅ 空文字列を含む列名を避ける
df.columns = [col if col.strip() != "" else "Unnamed" for col in df.columns]

# 書き込むデータ
data = [df.columns.tolist()] + df.values.tolist()

# ✅ gspread の順番通りに範囲→値を明示的に渡す
sheet.update(range_name="A1", values=data)

print("✅ 完了しました！Google Sheets にデータが正常に書き込まれました。")
