import pandas as pd
import yfinance as yf

df = yf.download('GOOGL', start='2026-01-01')

print(df.head())