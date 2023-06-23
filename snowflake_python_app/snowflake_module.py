import pandas as pd
import numpy as np

from logger import Logger

def connect_snowflake_accout(account, user, password, warehouse, database, schema):
    """
    Connect to Snowflake account
    """
    import snowflake.connector
    ctx = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )
    return ctx


## class to read data from snowflake and have two methods handle the data
class SnowflakeData:
    def __init__(self, account: str, user: str, password: str, warehouse: str, database: str, schema: str):
        """
        Connect to Snowflake account. To create Snowfalek account, please refer to https://www.snowflake.com/
        
        Args:
            account (str): Snowflake account
            user (str): Snowflake user
            password (str): Snowflake password
            warehouse (str): Snowflake warehouse
            database (str): Snowflake database
            schema (str): Snowflake schema
            """
        # initiate the logger
        self.log = Logger("snowflake.log")
        self.ctx:str = connect_snowflake_accout()
        self.account:str = account
        self.user:str = user
        self.password:str = password
        self.warehouse:str = warehouse
        self.database:str = database
        self.schema:str = schema

    def read_table(self, table_name: str, num_rows: int = 1000):
        """
        Read data from Snowflake table
        
        Args:
            table_name (str): Snowflake table name
            num_rows (int): number of rows to read from Snowflake table
        """
        ## Adding try catch to handle the error
        try:
            self.log.log(f"Reading {num_rows} rows from {table_name} table")
            df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT {num_rows}", self.ctx)
            return df
        except Exception as e:
            self.log.log(f"Error: {e}", level="ERROR")
            raise e
      
    
    def read_query(self, query: str):
        """
        Read data from Snowflake table
        
        Args:
            query (str): Snowflake
        """
        try:
            self.log.log(f"Reading data from Snowflake query")
            df = pd.read_sql(query, self.ctx)
            return df
        except Exception as e:
            self.log.log(f"Error: {e}", level="ERROR")
            raise e
    
    def write_table(self, df: pd.DataFrame, table_name: str):
        """
        Write data to Snowflake table
        
        Args:
            df (pd.DataFrame): pandas DataFrame
            table_name (str): Snowflake table name
        """
        try:
            self.log.log(f"Writing data to {table_name} table")
            df.to_sql(table_name, self.ctx, if_exists="replace")
        except Exception as e:
            self.log.log(f"Error: {e}", level="ERROR")
            raise e
        
    def update_table(self, df: pd.DataFrame, table_name: str):
        """
        Update data to Snowflake table
        
        Args:
            df (pd.DataFrame): pandas DataFrame
            table_name (str): Snowflake table name
        """
        try:
            self.log.log(f"Updating data to {table_name} table")
            df.to_sql(table_name, self.ctx, if_exists="append")
        except Exception as e:
            self.log.log(f"Error: {e}", level="ERROR")
            raise e
        
    def delete_table(self, table_name: str):
        """
        Delete data from Snowflake table
        
        Args:
            table_name (str): Snowflake table name
        """
        try:
            self.log.log(f"Deleting data from {table_name} table")
            self.ctx.cursor().execute(f"DELETE FROM {table_name}")
        except Exception as e:
            self.log.log(f"Error: {e}", level="ERROR")
            raise e
    

    