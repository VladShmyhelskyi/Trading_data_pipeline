import os
import snowflake.connector
from dotenv import load_dotenv

# Завантажуємо змінні середовища з файлу .env у корені проєкту
load_dotenv()

# Підключення до Snowflake через змінні середовища
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema="SILVER"
)

cur = conn.cursor()

try:
    print("Запуск трансформації шару Silver у Snowflake...")

    # Виконуємо SQL-запит очищення та збагачення даних
    silver_query = """
        CREATE OR REPLACE TABLE SILVER.cleaned_market_ticks AS
        WITH deduped_data AS (
            SELECT 
                timestamp,
                symbol,
                open_price,
                high_price,
                low_price,
                close_price,
                volume,
                ROW_NUMBER() OVER (PARTITION BY symbol, timestamp ORDER BY timestamp DESC) as rn
            FROM BRONZE.raw_market_ticks
            WHERE timestamp IS NOT NULL 
              AND close_price > 0
        )
        SELECT 
            timestamp,
            symbol,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
            ROUND(high_price - low_price, 5) AS price_spread,
            ROUND(close_price - open_price, 5) AS price_change,
            CURRENT_TIMESTAMP() AS processed_at
        FROM deduped_data
        WHERE rn = 1;
    """

    cur.execute(silver_query)
    print("Шар Silver успішно оновлено через Python-пайплайн!")

finally:
    cur.close()
    conn.close()