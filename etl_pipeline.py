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

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.company_name}&apikey={API_KEY}"
        print("url", type(url), url)

        response = requests.get(url)
        print("response", type(response), response)

        data_json = response.json()
        print("data_json", type(data_json), data_json)

        # print(data_json['Meta Data'])
        # print(data_json['Time Series (Daily)'])

        df_data = pd.DataFrame(data_json['Time Series (Daily)'])
        print("df_data", type(df_data),'\n' , df_data)

        df = df_data.copy()
        df = df.transpose()
        print("df", type(df),'\n' , df)

        df['last_refreshed'] = data_json['Meta Data']['3. Last Refreshed']
        df['symbol'] = data_json['Meta Data']['2. Symbol']
        df['time_zone'] = data_json['Meta Data']['5. Time Zone']
        print("df", type(df),'\n' , df.dtypes, '\n', df)

        print("df.columns", type(df.columns), '\n', df.columns)
        df.columns = df.columns.str.split().str[1]
        print("df.columns", type(df.columns), '\n', df.columns)



       


if __name__ == '__main__':
    etl = ETLStockMarket("IBM")
    etl.extract()