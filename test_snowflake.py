import os

import snowflake.connector

# Підключення до Snowflake через змінні середовища
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema="SILVER"
)

try:
    # Перевірка з'єднання простим запитом
    cur = conn.cursor()
    cur.execute("SELECT CURRENT_VERSION(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
    row = cur.fetchone()
    print("Успішне підключення до Snowflake!")
    print(f"Версія Snowflake: {row[0]}")
    print(f"Поточна база: {row[1]}, Схема: {row[2]}")
finally:
    cur.close()
    conn.close()