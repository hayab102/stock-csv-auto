import yfinance as yf
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# ① 取得する銘柄リスト（任意で追加）
tickers = ['6758.T', '9984.T', '7203.T']  # Sony, SoftBank, Toyotaなど

# ② 過去◯日分のデータ（例：過去10営業日）
period_days = 10

# ③ DataFrameに全銘柄のデータを結合
all_data = []

for ticker in tickers:
    df = yf.download(ticker, period=f'{period_days}d')
    df.reset_index(inplace=True)
    df['ticker'] = ticker  # ← 確実に追加
    all_data.append(df)

# ④ 結合して1つのCSVに
final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv("stock.csv", index=False)
print("✅ stock.csv saved.")

# ⑤ Googleスプレッドシート連携
try:
    # 環境変数に埋め込んだJSONキーを読み込み
    creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # スプレッドシート操作
    sheet = client.open("Stock Data Sheet")  # スプレッドシート名に注意
    worksheet = sheet.sheet1
    worksheet.clear()

    # tickerを含め全列を文字列としてアップロード（←これが重要）
    values = [final_df.columns.tolist()] + final_df.astype(str).values.tolist()
    worksheet.update(values)

    print("✅ スプレッドシートに更新完了。")
except Exception as e:
    print("❌ スプレッドシート更新エラー:", e)


