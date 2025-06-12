import yfinance as yf
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# 銘柄リスト
tickers = ['6758.T', '9984.T', '7203.T']  # ソニー, ソフトバンクG, トヨタ

frames = []

for ticker in tickers:
    df = yf.download(ticker, period='10d', interval='1d')
    df.reset_index(inplace=True)
    df['ticker'] = ticker
    frames.append(df)

final_df = pd.concat(frames)
final_df.reset_index(drop=True, inplace=True)

# CSV保存
final_df.to_csv('stock.csv', index=False)
print("✅ stock.csv saved.")

# Googleスプレッドシートにアップロード
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

spreadsheet = client.open("stock_sheet")  # 任意のスプレッドシート名に変更可
try:
    worksheet = spreadsheet.worksheet("Sheet1")
except:
    worksheet = spreadsheet.add_worksheet(title="Sheet1", rows="100", cols="20")

worksheet.clear()

# スプレッドシートへ書き込み
values = [final_df.columns.tolist()] + final_df.astype(str).values.tolist()
worksheet.update(values)
print("✅ スプレッドシートにアップロード完了")



