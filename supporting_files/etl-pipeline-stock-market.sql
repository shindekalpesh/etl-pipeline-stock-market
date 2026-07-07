SHOW DATABASES;

CREATE DATABASE bronze;

USE bronze;

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