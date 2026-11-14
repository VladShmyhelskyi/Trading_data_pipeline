import os
import snowflake.connector
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv

# Завантажуємо змінні з файлу .env у корені проєкту
load_dotenv()

# 1. Підключення до Snowflake (шар BRONZE) через змінні середовища
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema="BRONZE"
)

cur = conn.cursor()

try:
    # 2. Створюємо сиру таблицю у шарі BRONZE, якщо її ще немає
    cur.execute("""
        CREATE OR REPLACE TABLE raw_market_ticks (
            timestamp TIMESTAMP_NTZ,
            open_price FLOAT,
            high_price FLOAT,
            low_price FLOAT,
            close_price FLOAT,
            volume INT,
            symbol STRING
        )
    """)
    print("Таблиця BRONZE.raw_market_ticks успішно ініціалізована.")

    # 3. Список трейдингових інструментів для завантаження
    tickers = ["EURUSD=X", "GBPUSD=X", "JPY=X"]

    for ticker in tickers:
        print(f"Завантаження даних для {ticker}...")
        data = yf.download(ticker, period="1mo", interval="1d")

        if data.empty:
            print(f"Попередження: Немає даних для {ticker}")
            continue

        print(f"Отримано рядків для {ticker}: {len(data)}")

        # 4. Записуємо дані рядок за рядком у Snowflake
        for index, row in data.iterrows():
            ts = index.strftime('%Y-%m-%d %H:%M:%S')
            op = float(row['Open'].iloc[0] if hasattr(row['Open'], 'iloc') else row['Open'])
            hi = float(row['High'].iloc[0] if hasattr(row['High'], 'iloc') else row['High'])
            lo = float(row['Low'].iloc[0] if hasattr(row['Low'], 'iloc') else row['Low'])
            cl = float(row['Close'].iloc[0] if hasattr(row['Close'], 'iloc') else row['Close'])
            vol = int(row['Volume'].iloc[0] if hasattr(row['Volume'], 'iloc') else row['Volume'])

            sql = f"""
                INSERT INTO raw_market_ticks (timestamp, open_price, high_price, low_price, close_price, volume, symbol)
                VALUES ('{ts}', {op}, {hi}, {lo}, {cl}, {vol}, '{ticker}')
            """
            cur.execute(sql)

        print(ticker + " успішно завантажено в базу.")

    print("Усі ринкові дані успішно завантажені у шар BRONZE Snowflake!")

finally:
    cur.close()
    conn.close()