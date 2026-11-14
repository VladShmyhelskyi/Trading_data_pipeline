-- 1. Перемикаємось на роль адміністратора
USE ROLE ACCOUNTADMIN;

-- 2. Створюємо економний обчислювальний кластер (Virtual Warehouse)
CREATE OR REPLACE WAREHOUSE TRADING_WH
WITH
    WAREHOUSE_SIZE = 'XSMALL'      -- Мінімальний розмір (1 кредит/год)
    AUTO_SUSPEND = 60              -- Автоматична зупинка через 60 секунд бездіяльності
    AUTO_RESUME = TRUE             -- Автоматичний запуск при надходженні запиту
    INITIALLY_SUSPENDED = TRUE     -- Не витрачати кредити прямо зараз при створенні
    COMMENT = 'Warehouse for Financial ETL Project';

-- 3. Створюємо базу даних для нашого трейдингового проєкту
CREATE OR REPLACE DATABASE TRADING_DWH;

-- 4. Створюємо три шари архітектури даних (Medallion Architecture)
CREATE OR REPLACE SCHEMA TRADING_DWH.BRONZE COMMENT = 'Сирі дані з API / PySpark';
CREATE OR REPLACE SCHEMA TRADING_DWH.SILVER COMMENT = 'Очищені та типізовані котирування';
CREATE OR REPLACE SCHEMA TRADING_DWH.GOLD   COMMENT = 'Агреговані вітрини даних для аналітики';

-- 5. Перевіряємо налаштування створеного кластера
SHOW WAREHOUSES LIKE 'TRADING_WH';