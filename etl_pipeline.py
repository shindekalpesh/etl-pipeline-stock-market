import os
from dotenv import load_dotenv

class ETLStockMarket:
    """
    Extracts, Transforms and Loads the stock market data of a given company.
    """
    def __init__(self, company_name):
        self.company_name = company_name

    def __str__(self):
        return f"company_name: {self.company_name}"
        