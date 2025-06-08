import yfinance as yf
import pandas as pd

# 取得する銘柄コード（例：ソニー 6758.T）
ticker = yf.Ticker("6758.T")

# 直近5日分の株価を取得
hist = ticker.history(period="5d")

# CSVファイルとして保存
hist.to_csv("stock.csv")

print("✅ stock.csv saved.")
