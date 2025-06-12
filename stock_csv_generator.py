import yfinance as yf
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# 1. データ取得対象の銘柄
tickers = ["6758.T", "7203.T"]  # ここに必要な銘柄を追加

# 2. 各銘柄の株価データを取得し、ticker列を追加
df_list = []
for ticker in tickers:
    data = yf.download(ticker, period="5d")
    if not data.empty:
        data["ticker"] = ticker
        data.reset_index(inplace=True)
        df_list.append(data)

# 3. データをまとめて1つのDataFrameに統合
if df_list:
    final_df = pd.concat(df_list)
    final_df.to_csv("stock.csv", index=False)
    print("✅ stock.csv saved.")
else:
    print("⚠️ No data fetched. Check ticker symbols or network issues.")
    exit()

# 4. スプレッドシート連携設定
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# 5. 環境変数から認証情報を取得
try:
    creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
except KeyError:
    print("❌ GOOGLE_CREDENTIALS not set in environment variables.")
    exit()

# 6. 認証してシート更新
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# 7. スプレッドシートへ反映（※シート名に注意）
try:
    sheet = client.open("Stock Data Sheet")  # スプレッドシート名を正確に
    worksheet = sheet.sheet1
    worksheet.clear()
    worksheet.update([final_df.columns.tolist()] + final_df.values.tolist())
    print("✅ スプレッドシートに更新完了。")
except Exception as e:
    print("❌ スプレッドシート更新エラー:", e)

