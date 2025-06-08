import yfinance as yf
import pandas as pd
from datetime import datetime

# 銘柄リスト（例：トヨタ、ソニー、任天堂など日本株なら証券コード.JP）
tickers = ['7203.T', '6758.T', '7974.T']

# 今日の日付（ファイル名に使う）
today = datetime.now().strftime('%Y-%m-%d')

# 期間や間隔を設定してデータ取得（1ヶ月間、日足）
data = yf.download(tickers, period="1mo", interval="1d", group_by='ticker', auto_adjust=True)

# 各銘柄ごとにCSV保存
for ticker in tickers:
    df = data[ticker].dropna()
    filename = f"{ticker.replace('.T', '')}_{today}.csv"
    df.to_csv(filename, encoding='utf-8-sig')
    print(f"{filename} を保存しました。")
