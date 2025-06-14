import yfinance as yf
import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

ticker = "AAPL"
df = yf.download(ticker, period="10d", interval="1d")

df.reset_index(inplace=True)
df = df.fillna("")
df = df.astype(str)

sheet = client.open("stock_sheet").sheet1
sheet.clear()

data = [df.columns.tolist()] + df.values.tolist()
sheet.update(range_name="A1", values=data)

print("✅ Google Sheets 更新成功")
