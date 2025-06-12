import yfinance as yf
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# 株式ティッカー（必要に応じて複数でもOK）
ticker = "6758.T"  # ソニーグループの例

# 株価データの取得（過去10日）
df = yf.download(ticker, period='10d', interval='1d')

# CSVとしてローカルに保存
df.to_csv('stock.csv')
print("✅ stock.csv saved.")

# --- Googleスプレッドシート連携 ---

# 認証用の環境変数（GitHub Secrets に登録したJSON）
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])

# 認証スコープの設定
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# ✅ ←ここを自分のスプレッドシート名に変更！
spreadsheet = client.open("stock_sheet")  # 例: "株価データ" など

# シートの選択（最初のワークシートを使用）
worksheet = spreadsheet.sheet1

# スプレッドシートをクリアしてから更新
worksheet.clear()
worksheet.update([df.reset_index().columns.values.tolist()] + df.reset_index().values.tolist())

print("✅ Googleスプレッドシートにデータを更新しました。")




