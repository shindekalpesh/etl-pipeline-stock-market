import os
from dotenv import load_dotenv

import requests

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

       


if __name__ == '__main__':
    etl = ETLStockMarket("IBM")
    etl.extract()