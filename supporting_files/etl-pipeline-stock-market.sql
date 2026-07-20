SHOW DATABASES;

CREATE DATABASE etl_stock_market;

USE etl_stock_market;

CREATE TABLE IF NOT EXISTS bronze_tbl (
	id INT PRIMARY KEY AUTO_INCREMENT,
    stock_date VARCHAR(20),
    open VARCHAR(20),
    high VARCHAR(20),
    low VARCHAR(20),
    close VARCHAR(20),
    volume VARCHAR(20), 
    last_refreshed VARCHAR(20),
	symbol VARCHAR(20),
	time_zone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS silver_tbl (
	id INT PRIMARY KEY AUTO_INCREMENT,
    stock_date DATETIME,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume NUMERIC, 
    last_refreshed DATETIME,
	symbol VARCHAR(10),
	time_zone VARCHAR(10),
    added_on DATETIME
);

ALTER TABLE silver_tbl
-- MODIFY stock_date DATE; 
MODIFY last_refreshed DATE;

SELECT *
FROM bronze_tbl;

TRUNCATE bronze_tbl;

SELECT *
FROM silver_tbl;

TRUNCATE silver_tbl;

COMMIT;