import yfinance as yf
import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# 認証情報（GitHub Secrets に格納した JSON を読み込む）
credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

# データ取得
ticker = "AAPL"
df = yf.download(ticker, period="10d", interval="1d")

# データ整形
df.reset_index(inplace=True)
df = df.fillna("")
df = df.astype(str)

# スプレッドシートに接続
sheet = client.open("stock_sheet").sheet1
sheet.clear()

# アップデート
data = [df.columns.tolist()] + df.values.tolist()
sheet.update(range_name="A1", values=data)  # ✅ 正しい順番で指定

print("✅ Google Sheets 更新成功")
