-- 1. Перемикаємось на роль адміністратора
USE ROLE ACCOUNTADMIN;

-- 2. Створюємо базу даних для трейдингового проєкту
CREATE OR REPLACE DATABASE TRADING_DWH;

-- 3. Створюємо три шари архітектури даних (Medallion Architecture)
CREATE OR REPLACE SCHEMA TRADING_DWH.BRONZE COMMENT = 'Сирі дані з API / PySpark';
CREATE OR REPLACE SCHEMA TRADING_DWH.SILVER COMMENT = 'Очищені та типізовані котирування';
CREATE OR REPLACE SCHEMA TRADING_DWH.GOLD   COMMENT = 'Агреговані вітрини даних для аналітики';