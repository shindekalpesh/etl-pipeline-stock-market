import os
from dotenv import load_dotenv

import requests
import json
import pandas as pd

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Numeric, DateTime, Date

from datetime import datetime

class ETLStockMarket:
    """
    Extracts, Transforms and Loads the stock market data of a given company.
    """
    def __init__(self, company_name):
        self.company_name = company_name

    def __str__(self):
        return f"company_name: {self.company_name}"

    @staticmethod
    def db_connection():
        # DATABASE_URL = os.getenv('DATABASE_URL')
        # DATABASE_URL="mysql://root:root1234@127.0.0.1:3306/bronze"
        load_dotenv()

        DB_CLIENT = os.getenv('DB_CLIENT')
        DB_USERNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_HOSTNAME = os.getenv('DB_HOSTNAME')
        DB_PORT = os.getenv('DB_PORT')
        DB_NAME = os.getenv('DB_NAME')
        
        # print("DB_CLIENT", type(DB_CLIENT), DB_CLIENT)
        # print("DB_USERNAME", type(DB_USERNAME), DB_USERNAME)
        # print("DB_PASSWORD", type(DB_PASSWORD), DB_PASSWORD)
        # print("DB_HOSTNAME", type(DB_HOSTNAME), DB_HOSTNAME)
        # print("DB_PORT", type(DB_PORT), DB_PORT)
        # print("DB_NAME", type(DB_NAME), DB_NAME)
        
        DATABASE_URL = f"{DB_CLIENT}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"


        engine = create_engine(DATABASE_URL)
        print("engine", type(engine), engine)

        return engine
        
    def extract(self):
        API_KEY = os.getenv('API_KEY')
        # DATABASE_URL = os.getenv('DATABASE_URL')
        # print("DATABASE_URL", type(DATABASE_URL), DATABASE_URL)
        
        # engine = create_engine(DATABASE_URL)
        # print("engine", type(engine), engine)

        engine = self.db_connection()
        print("engine", type(engine), engine)

        # breakpoint()
        # print("self.company_name", type(self.company_name), self.company_name)

        # url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.company_name}&apikey={API_KEY}"
        # print("url", type(url), url)

        # response = requests.get(url)
        # print("response", type(response), response)

        # data_json = response.json()
        # print("data_json", type(data_json), data_json)

        
        data_json = {
            "Meta Data": {
                "1. Information": "Daily Prices (open, high, low, close) and Volumes",
                "2. Symbol": "IBM",
                "3. Last Refreshed": "2026-07-02",
                "4. Output Size": "Compact",
                "5. Time Zone": "US/Eastern"
            },
            "Time Series (Daily)": {
                "2026-07-02": {
                    "1. open": "283.1400",
                    "2. high": "290.9300",
                    "3. low": "282.2800",
                    "4. close": "289.5200",
                    "5. volume": "5950158"
                },
                "2026-07-01": {
                    "1. open": "279.6600",
                    "2. high": "294.4900",
                    "3. low": "278.9600",
                    "4. close": "286.2500",
                    "5. volume": "6905811"
                },
                "2026-06-30": {
                    "1. open": "273.2100",
                    "2. high": "282.5694",
                    "3. low": "271.1200",
                    "4. close": "281.2100",
                    "5. volume": "7458360"
                },
                "2026-06-29": {
                    "1. open": "274.3000",
                    "2. high": "278.1500",
                    "3. low": "269.0600",
                    "4. close": "278.0000",
                    "5. volume": "6464204"
                },
                "2026-06-26": {
                    "1. open": "258.9400",
                    "2. high": "273.1350",
                    "3. low": "258.2800",
                    "4. close": "271.6300",
                    "5. volume": "9719927"
                }
            }
        }
        # print("data_json", type(data_json), data_json)

        # breakpoint()

        # print(data_json['Meta Data'],"\n\n")
        # print(data_json['Time Series (Daily)'],"\n\n")

        df_data = pd.DataFrame(data_json['Time Series (Daily)'])
        # print("df_data STOCK", type(df_data), '\n', df_data.dtypes, "\n", df_data.shape, "\n", df_data)

        df_safe = df_data.copy()
        # print("df BEFORE T", type(df),'\n' , df)
        df = df_safe.T.reset_index()
        df = df.rename(columns={"index": "stock_date"})
        # print("df AFTER T", type(df),'\n' , df)

        df['last_refreshed'] = data_json['Meta Data']['3. Last Refreshed']
        df['symbol'] = data_json['Meta Data']['2. Symbol']
        df['time_zone'] = data_json['Meta Data']['5. Time Zone']

        # print("df.columns", type(df.columns), '\n', df.columns)
        df.columns = ['stock_date', 'open', 'high', 'low', 'close', 'volume',
       'last_refreshed', 'symbol', 'time_zone']
        # print("df.columns", type(df.columns), '\n', df.columns)

        # print("df.shape", type(df.shape), '\n', df.shape)

        print("df", type(df),'\n' , df.dtypes, '\n', df)
        
        try:
            df.to_sql(name='bronze_tbl', con=engine, if_exists='append', index=False, chunksize=10)
            print(f"Data added successfully to the bronze layer.")

        except Exception as e:
            print(f"Error occured: {e}")

    
    def transform(self):
        engine = self.db_connection()
        bronze_df = pd.read_sql("SELECT * FROM bronze_tbl", con=engine)
        
        print("TRANSFORM LAYER -1 > bronze_df", type(bronze_df),'\n' , bronze_df.dtypes, '\n', bronze_df)
        silver_df = pd.DataFrame()

        # bronze_df['id'] = bronze_df['id']
        silver_df['stock_date'] = pd.to_datetime(bronze_df['stock_date'],format="%Y-%m-%d",errors='coerce').dt.date
        silver_df['open'] = pd.to_numeric(bronze_df['open'],errors='coerce')
        silver_df['high'] = pd.to_numeric(bronze_df['high'],errors='coerce')
        silver_df['low'] = pd.to_numeric(bronze_df['low'],errors='coerce')
        silver_df['close'] = pd.to_numeric(bronze_df['close'],errors='coerce')
        silver_df['volume'] = pd.to_numeric(bronze_df['volume'],errors='coerce')
        silver_df['last_refreshed'] = pd.to_datetime(bronze_df['last_refreshed'],format="%Y-%m-%d",errors='coerce').dt.date
        silver_df['symbol'] = bronze_df['symbol']
        silver_df['time_zone'] = bronze_df['time_zone']
        silver_df['added_on'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")                  # to be added

        print("TRANSFORM LAYER - 2 > silver_df", type(silver_df),'\n' , silver_df.dtypes, '\n', silver_df)

        try:
            silver_df.to_sql(name='silver_tbl', con=engine, if_exists='append', index=False, chunksize=10)
            print(f"Data added successfully to the silver layer.")

        except Exception as e:
            print(f"Error occured: {e}")


    def load(self):
        engine = self.db_connection()
        silver_df = pd.read_sql("SELECT * FROM silver_tbl", con=engine)

        # gold_df = pd.DataFrame()

        gold_df = silver_df

        # Calculate 7-day rolling mean
        gold_df['close_rolling_7d_mean'] = silver_df['close'].rolling(window=7).mean()

        # Calculate 7-day rolling sum
        gold_df['close_rolling_7d_sum'] = silver_df['close'].rolling(window=7).sum()


        try:
            gold_df.to_sql(name="gold_tbl", con=engine, if_exists='append', index=False, chunksize=100)
            print(f"Data added successfully to the silver layer.")

        except Exception as e:
            print(f"Error occured: {e}")

if __name__ == '__main__':
    etl = ETLStockMarket("IBM")
    etl.extract()
    etl.transform()
    etl.load()