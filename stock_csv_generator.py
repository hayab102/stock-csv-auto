import yfinance as yf
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# --- 1. 対象のティッカーコード（複数可）
tickers = ["6758.T", "7203.T"]  # 例：ソニー、トヨタ

# --- 2. データを取得して整形
df_list = []
for ticker in tickers:
    df = yf.download(ticker, period="5d")
    df["ticker"] = ticker  # ★ ticker列を追加
    df.reset_index(inplace=True)
    df_list.append(df)

final_df = pd.concat(df_list)

# --- 3. CSV出力
final_df.to_csv("stock.csv", index=False)
print("✅ stock.csv saved.")

# --- 4. スプレッドシート連携
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# 認証情報を読み込む
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# スプレッドシートとワークシートを指定
spreadsheet = client.open("Stock Data Sheet")  # ★スプレッドシート名
worksheet = spreadsheet.sheet1

# 既存データをクリアして書き込む
worksheet.clear()
worksheet.update([final_df.columns.values.tolist()] + final_df.values.tolist())
