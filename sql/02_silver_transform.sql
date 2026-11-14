-- 1. Перемикаємо контекст
USE DATABASE TRADING_DWH;
USE WAREHOUSE TRADING_WH;

-- 2. Створюємо / перезаписуємо таблицю у шарі SILVER з очищенням та збагаченням
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
        -- Використовуємо віконну функцію для видалення можливих дублів за унікальним таймстампом та тикером
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
    -- Додаємо аналітичні розрахунки (інженерне збагачення даних)
    ROUND(high_price - low_price, 5) AS price_spread, -- Спред свічки (волатильність)
    ROUND(close_price - open_price, 5) AS price_change, -- Зміна ціни за період
    CURRENT_TIMESTAMP() AS processed_at               -- Системна мітка часу обробки
FROM deduped_data
WHERE rn = 1; -- Залишаємо лише унікальні записи

-- 3. Робимо перевірку результату у Silver
SELECT * FROM SILVER.cleaned_market_ticks LIMIT 10;