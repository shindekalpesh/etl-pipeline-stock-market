import os
from dotenv import load_dotenv

import requests
import json
import pandas as pd

class ETLStockMarket:
    """
    Extracts, Transforms and Loads the stock market data of a given company.
    """
    def __init__(self, company_name):
        self.company_name = company_name

    def __str__(self):
        return f"company_name: {self.company_name}"
        
    def extract(self):
        load_dotenv()
        API_KEY = os.getenv('API_KEY')

        print("self.company_name", type(self.company_name), self.company_name)

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
        


if __name__ == '__main__':
    etl = ETLStockMarket("IBM")
    etl.extract()