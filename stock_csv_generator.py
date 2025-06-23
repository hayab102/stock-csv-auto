import yfinance as yf
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from ta.momentum import RSIIndicator  # ← 追加

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
cols = ["ticker"] + [col for col in df.columns if col != "ticker"]
df = df[cols]

# インデックスを列に戻す（Date を含める）
df.reset_index(inplace=True)

# ✅ RSI + MA5 のテクニカル指標を計算（追加処理ここから）
df["Close"] = df["Close"].astype(float)
df["MA5"] = df["Close"].rolling(window=5).mean()
df["RSI"] = RSIIndicator(close=df["Close"], window=14).rsi()

# ✅ 勝ち条件：「終値 > MA5」かつ「RSI < 50」
df["勝ち"] = ((df["Close"] > df["MA5"]) & (df["RSI"] < 50)).astype(int)
# ✅ 追加処理ここまで

# NaN → 空文字, すべて文字列へ
df = df.fillna("").astype(str)

# ✅ 列名を文字列として扱い、空文字を除外
df.columns = [str(col).strip() if str(col).strip() != "" else "Unnamed" for col in df.columns]

# Google Sheets に書き込む形式に
data = [df.columns.tolist()] + df.values.tolist()

# シートをクリアして書き込み（ここはそのまま維持）
sheet.clear()
sheet.update(data)

print("✅ Google Sheets に株データ＋勝率列を更新しました。")
