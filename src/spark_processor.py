import os
import tempfile
import pandas as pd
import yfinance as yf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round as spark_round
from dotenv import load_dotenv

# Фікс для Windows (Hadoop home)
hadoop_dir = os.path.join(tempfile.gettempdir(), "hadoop")
os.makedirs(os.path.join(hadoop_dir, "bin"), exist_ok=True)
os.environ['HADOOP_HOME'] = hadoop_dir


def main():
    # 1. Ініціалізація локальної сесії Apache Spark з вимкненою перевіркою для Windows
    spark = SparkSession.builder \
        .appName("TradingDataSparkProcessor") \
        .master("local[*]") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .config("spark.sql.warehouse.dir", "file:///C:/temp") \
        .getOrCreate()

    print("🚀 Apache Spark сесія успішно запущена локально!")

    # 2. Збираємо сирі дані через yfinance для прикладу
    ticker = "EURUSD=X"
    print(f"Завантаження даних для {ticker} через Python...")
    raw_pd = yf.download(ticker, period="3mo", interval="1d")

    if raw_pd.empty:
        print("Попередження: Немає даних для обробки.")
        spark.stop()
        return

    # Очищуємо мультиіндексні колонки yfinance
    if isinstance(raw_pd.columns, pd.MultiIndex):
        raw_pd.columns = raw_pd.columns.droplevel(1)

    raw_pd = raw_pd.reset_index()
    raw_pd.columns = [str(c).lower() for c in raw_pd.columns]
    raw_pd['symbol'] = ticker

    # 3. Конвертуємо Pandas DataFrame у розподілений Spark DataFrame
    spark_df = spark.createDataFrame(raw_pd)
    print(f"Оригінальна кількість рядків у Spark DataFrame: {spark_df.count()}")

    # 4. Виконуємо трансформації за допомогою PySpark DataFrame API (Silver шар)
    print("Виконання розподілених трансформацій та очищення даних у Spark...")
    cleaned_spark_df = spark_df \
        .filter(col("close").isNotNull() & (col("close") > 0)) \
        .withColumn("price_spread", spark_round(col("high") - col("low"), 5)) \
        .withColumn("price_change", spark_round(col("close") - col("open"), 5)) \
        .select("date", "symbol", "open", "high", "low", "close", "volume", "price_spread", "price_change")

    # Показуємо перші 5 рядків оброблених даних у консолі
    cleaned_spark_df.show(5, truncate=False)

    # 5. Зберігаємо результати: конвертуємо у Pandas і записуємо у CSV-формат
    output_path = "data/processed_market_data.csv"

    # Створюємо папку data, якщо її немає
    os.makedirs("data", exist_ok=True)

    # Переводимо оброблений Spark DataFrame у Pandas і зберігаємо у CSV
    cleaned_pd_df = cleaned_spark_df.toPandas()
    cleaned_pd_df.to_csv(output_path, index=False)

    print(f"Дані успішно оброблені через Spark і збережені у файл: {output_path}")

    # Зупиняємо Spark сесію
    spark.stop()


if __name__ == "__main__":
    main()