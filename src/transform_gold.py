import os
import snowflake.connector
from dotenv import load_dotenv

# Завантажуємо змінні середовища з файлу .env
load_dotenv()

# Підключення до Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema="GOLD"
)

cur = conn.cursor()

try:
    print("Запуск побудови вітрини даних Gold (Data Mart) у Snowflake...")

    gold_query = """
        CREATE OR REPLACE TABLE GOLD.market_summary_mart AS
        SELECT 
            symbol,
            DATE(timestamp) AS trade_date,
            COUNT(*) AS total_ticks,
            ROUND(AVG(close_price), 5) AS avg_close_price,
            ROUND(MAX(high_price), 5) AS max_high_price,
            ROUND(MIN(low_price), 5) AS min_low_price,
            ROUND(AVG(price_spread), 5) AS avg_spread,
            SUM(volume) AS total_volume
        FROM SILVER.cleaned_market_ticks
        GROUP BY symbol, DATE(timestamp);
    """

    cur.execute(gold_query)
    print("Вітрина Gold успішно побудована та оновлена!")

finally:
    cur.close()
    conn.close()