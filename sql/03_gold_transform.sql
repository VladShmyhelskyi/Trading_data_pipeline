-- 1. Перемикаємо контекст на нашу базу та склад
USE DATABASE TRADING_DWH;
USE WAREHOUSE TRADING_WH;

-- 2. Створюємо / перезаписуємо фінальну агреговану вітрину у шарі GOLD
CREATE OR REPLACE TABLE GOLD.market_summary_mart AS
SELECT
    symbol,
    DATE(timestamp) AS trade_date,
    COUNT(*) AS total_ticks,                         -- Кількість тіків (зрізів) за день
    ROUND(AVG(close_price), 5) AS avg_close_price,   -- Середня ціна закриття
    ROUND(MAX(high_price), 5) AS max_high_price,     -- Максимальна ціна дня
    ROUND(MIN(low_price), 5) AS min_low_price,       -- Мінімальна ціна дня
    ROUND(AVG(price_spread), 5) AS avg_spread,       -- Середній спред (волатильність)
    SUM(volume) AS total_volume                      -- Сумарний обсяг торгів
FROM SILVER.cleaned_market_ticks
GROUP BY symbol, DATE(timestamp);

-- 3. Робимо перевірку фінальної вітрини
SELECT * FROM GOLD.market_summary_mart;