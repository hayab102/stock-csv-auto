import yfinance as yf
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from ta.momentum import RSIIndicator

# 認証
credentials_dict = json.loads(os.environ['GOOGLE_CREDENTIALS'])
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
gc = gspread.authorize(credentials)

# スプレッドシートに接続
spreadsheet = gc.open("stock_sheet")  # ← スプレッドシート名（必要に応じて変更）
sheet = spreadsheet.sheet1

# 株価データを取得
ticker = "7203.T"
df = yf.download([ticker], period="10d", interval="1d")
df.columns = df.columns.get_level_values(0)
df.reset_index(inplace=True)
df["ticker"] = ticker

# 列の順番を整える（tickerを2列目へ）
df = df[["Date", "ticker", "Open", "High", "Low", "Close", "Volume"]]

# テクニカル指標計算（移動平均＋RSI）
df["Close"] = df["Close"].astype(float)
df["MA5"] = df["Close"].rolling(window=5).mean()
df["RSI"] = RSIIndicator(close=df["Close"], window=14).rsi()
df["勝ち"] = ((df["Close"] > df["MA5"]) & (df["RSI"] < 50)).astype(int)

# 列の順番を最終調整（全部10列）
df = df[["Date", "ticker", "Open", "High", "Low", "Close", "Volume", "MA5", "RSI", "勝ち"]]

# ✅ 列名を日本語に変換（ヘッダー行）
df.columns = ["日付", "銘柄", "始値", "高値", "安値", "終値", "出来高", "移動平均", "RSI", "勝ち"]

# NaN → 空文字, すべて文字列化
df = df.fillna("").astype(str)

# Google Sheets に書き込む形式に変換
data = [df.columns.tolist()] + df.values.tolist()

# シート更新
sheet.clear()
sheet.update(data)

print("✅ Google Sheets に日本語ヘッダーで株データを更新しました。")
