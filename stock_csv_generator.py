import yfinance as yf
import pandas as pd

# 取得する銘柄コード（例：ソニー 6758.T）
ticker = yf.Ticker("6758.T")

# 直近5日分の株価を取得
hist = ticker.history(period="5d")

# CSVファイルとして保存
hist.to_csv("stock.csv")

print("✅ stock.csv saved.")
# 以下をファイルの末尾に追加（既にある場合は不要）
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets 連携設定
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('my-credentials.json', scope)
client = gspread.authorize(creds)

spreadsheet = client.open("stock-auto-g.csv")
worksheet = spreadsheet.sheet1
worksheet.clear()

with open('stock.csv', newline='', encoding='utf-8') as csvfile:
    import csv
    reader = csv.reader(csvfile)
    rows = list(reader)
    worksheet.update('A1', rows)
