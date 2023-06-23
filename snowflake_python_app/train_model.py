from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

from logger import Logger
from snowflake_module import SnowflakeData

from typing import List

table_name:str = "SALES"
num_rows:int = 1000
columns:List(str) = ["SALES", "PROFIT", "QUANTITY", "DISCOUNT", "PRODUCT_ID", "CUSTOMER_ID", "ORDER_ID", "ORDER_DATE", "SHIP_DATE", "SHIP_MODE", "CUSTOMER_NAME", "SEGMENT", "COUNTRY", "CITY", "STATE", "POSTAL_CODE", "REGION", "PRODUCT_NAME", "CATEGORY", "SUB_CATEGORY", "PRODUCT_BASE_MARGIN", "SHIPPER_NAME", "MONTH", "YEAR"]

# initiate the logger
log = Logger("snowflake.log")
log.log("Start reading data from Snowflake table")

## Class to read data, clean it, and split it into train and test
class Data:
    def __init__(self, table_name: str, num_rows: int = 1000):
        """
        Read data from Snowflake table"""
        self.log:Logger = Logger("snowflake.log")
        self.log.log("Start reading data from Snowflake table")
        self.table_name:str = table_name
        self.num_rows:int = num_rows
        self.columns:List(str) = columns
        self.df:pd.DataFrame = SnowflakeData().read_table(self.table_name, self.num_rows)


    def clean_data(self):
        """
        Clean data
        """
        self.log.log("Start cleaning data")
        self.df:pd.DataFrame = self.df[self.columns]
        self.df["ORDER_DATE"] = pd.to_datetime(self.df["ORDER_DATE"])
        self.df["SHIP_DATE"] = pd.to_datetime(self.df["SHIP_DATE"])
        self.df["MONTH"] = self.df["ORDER_DATE"].dt.month
        self.df["YEAR"] = self.df["ORDER_DATE"].dt.year
        self.df["SALES"] = self.df["SALES"].str.replace("$", "").str.replace(",", "").astype(float)
        self.df["PROFIT"] = self.df["PROFIT"].str.replace("$", "").str.replace(",", "").astype(float)
        self.df["PRODUCT_BASE_MARGIN"] = self.df["PRODUCT_BASE_MARGIN"].str.replace("$", "").str.replace(",", "").astype(float)
        self.log.log("Finish cleaning data")
    
    def create_date_features(self):
        """
        Create date features
        """
        self.log.log("Start creating date features")
        self.df["ORDER_DATE"] = pd.to_datetime(self.df["ORDER_DATE"])
        self.df["SHIP_DATE"] = pd.to_datetime(self.df["SHIP_DATE"])
        self.df["MONTH"] = self.df["ORDER_DATE"].dt.month
        self.df["YEAR"] = self.df["ORDER_DATE"].dt.year
        self.log.log("Finish creating date features")
        
    def create_sales_features(self):
        """
        Create sales features
        """
        self.log.log("Start creating sales features")
        self.df["SALES"] = self.df["SALES"].str.replace("$", "").str.replace(",", "").astype(float)
        self.df["PROFIT"] = self.df["PROFIT"].str.replace("$", "").str.replace(",", "").astype(float)
        self.df["PRODUCT_BASE_MARGIN"] = self.df["PRODUCT_BASE_MARGIN"].str.replace("$", "").str.replace(",", "").astype(float)
        self.log.log("Finish creating sales features")

    
    def split_data(self):
        """
        Split data into train and test
        """
        self.log.log("Start splitting data into train and test")
        X = self.df.drop(["SALES"], axis=1)
        y = self.df["SALES"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
        self.log.log("Finish splitting data into train and test")
        return X_train, X_test, y_train, y_test