import os
import re
import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf

from .icomponent import IComponent


# The `Stock` class represents a stock with methods to calculate daily returns, compound annual growth
# rate (CAGR), and standard deviation.
# This class represents a stock and implements the IComponent interface.
class Stock(IComponent):
    def __init__(self, name: str, df: pd.DataFrame) -> None:
        """
        This function initializes an object with a name and a DataFrame, performing validation checks on
        the DataFrame columns.
        
        :param name: The `name` parameter is a string that represents the name of the object being
        initialized in the class
        :type name: str
        :param df: The `df` parameter is expected to be a Pandas DataFrame object containing financial
        data. The DataFrame should have columns named "Date", "Open", and "Close". If the DataFrame
        provided does not meet these requirements, exceptions will be raised
        :type df: pd.DataFrame
        """
        # This code snippet is performing a validation check to ensure that the input parameter `df`
        # is of type `pd.DataFrame`.
        if not type(df)==pd.DataFrame:
            raise Exception("Pass DataFrame Object")
        # This code snippet is performing a validation check on the DataFrame columns to ensure that
        # it contains the required columns "Date", "Open", and "Close".
        if not set(df.columns).issuperset(set(["Date", "Open", "Close"])):
            raise Exception("DataFrame should contain Date, Open, Close Columns")
        self.name=name
        self.__df = df.sort_values(by="Date")
    
    def __repr__(self) -> str:
        """
        The `__repr__` function in Python returns a string representation of an object, specifically for
        a Stock object with its name.
        :return: The `__repr__` method is returning a string representation of the object in the format
        "Stock[name]", where `name` is the name attribute of the object.
        """
        return f"Stock[{self.name}]"
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        The function `get_dataframe` returns the DataFrame stored in the object.
        :return: A pandas DataFrame is being returned.
        """
        return self.__df
    
    def get_daily_return(self) -> pd.Series:
        """
        The function calculates the daily return percentage based on the opening and closing prices in a
        DataFrame.
        :return: A pandas Series containing the daily returns calculated based on the difference between
        the "Close" and "Open" prices in the DataFrame (__df) provided to the function.
        """
        # The lines `initial_value = self.__df["Open"]` and `final_value = self.__df["Close"]` are
        # extracting the "Open" and "Close" prices from the DataFrame stored in the Stock object.
        initial_value = self.__df["Open"]
        final_value = self.__df["Close"]

        # The line `return_daily = ((final_value-initial_value)/initial_value)*100` in the
        # `get_daily_return` method of the `Stock` class is calculating the daily return percentage
        # based on the opening and closing prices in the DataFrame.
        return_daily = ((final_value-initial_value)/initial_value)*100
        # The line `return_daily = pd.Series(return_daily.to_list(), index=self.__df.Date.to_list())`
        # in the `get_daily_return` method of the `Stock` class is creating a pandas Series object
        # with the daily return values calculated based on the difference between the "Close" and
        # "Open" prices in the DataFrame provided to the function.
        return_daily = pd.Series(return_daily.to_list(), index=self.__df.Date.to_list())

        return return_daily
    
    def get_cagr(self) -> np.float64:
        """
        The `get_cagr` function calculates the Compound Annual Growth Rate (CAGR) based on opening and
        closing prices from a DataFrame stored in a Stock object.
        :return: The `get_cagr` method of the `Stock` class is returning the Compound Annual Growth Rate
        (CAGR) calculated based on the opening and closing prices from the DataFrame stored in the Stock
        object. The formula used to calculate the CAGR is `pow((final_value/initial_value),
        (1/total_year))-1`.
        """
        # The lines `initial_value = self.__df["Open"].iloc[0]` and `final_value =
        # self.__df["Close"].iloc[-1]` in the `get_cagr` method of the `Stock` class are extracting
        # the initial and final values for the calculation of the Compound Annual Growth Rate (CAGR)
        # based on the opening and closing prices from the DataFrame stored in the Stock object.
        initial_value = self.__df["Open"].iloc[0]
        final_value = self.__df["Close"].iloc[-1]

        # The code snippet `year = pd.to_datetime(self.__df["Date"]).dt.year` is converting the "Date"
        # column in the DataFrame stored in the Stock object to a datetime format and then extracting
        # the year component from each date.
        year = pd.to_datetime(self.__df["Date"]).dt.year
        total_year = len(year.unique())
        # The expression `return pow((final_value/initial_value), (1/total_year))-1` is calculating
        # the Compound Annual Growth Rate (CAGR) of a financial dataset in the `get_cagr` method of
        # the `Stock` class.
        return pow((final_value/initial_value), (1/total_year))-1
    
    def get_std(self) -> np.float64:
        """
        This function calculates the standard deviation of daily returns.
        :return: The code is returning the standard deviation of the daily returns for a given object.
        """
        return self.get_daily_return().std()


# This Python class `StockFactory` is designed to create instances of `Stock` by downloading and
# loading stock data from Yahoo Finance.
class StockFactory:
    def __init__(self, start_date: dt.datetime, end_date: dt.datetime, freq: str) -> None:
        """
        This function initializes an object with start date, end date, and frequency attributes.
        
        :param start_date: The `start_date` parameter is a datetime object representing the start date
        of a time period
        :type start_date: dt.datetime
        :param end_date: The `end_date` parameter in the `__init__` method is of type `dt.datetime`,
        which indicates that it is expected to be a datetime object representing the end date of a time
        period. This parameter is used to store the end date value for the object being initialized
        :type end_date: dt.datetime
        :param freq: The `freq` parameter in the `__init__` method is used to specify the frequency of
        the date range. It could be daily, weekly, monthly, etc., depending on the requirements of your
        application. This parameter allows you to define how the date range should be divided or
        incremented
        :type freq: str
        """
        self.start_date = start_date
        self.end_date = end_date
        self.freq = freq

    def __download_data(self, stock_name: str, file_path: os.path) -> None:
        """
        The function downloads stock data for a given stock name and saves it to a specified file path.
        
        :param stock_name: The `stock_name` parameter is a string that represents the name of the stock
        for which you want to download data
        :type stock_name: str
        :param file_path: The `file_path` parameter in the `__download_data` method is expected to be of
        type `os.path`, which typically represents a file path in the operating system. This parameter
        should contain the location where the downloaded data will be saved as a CSV file
        :type file_path: os.path
        """
        if(type(stock_name)==str):
            df = yf.download(
                tickers=stock_name, 
                start=self.start_date, 
                end=self.end_date,
                interval=self.freq
            )

            df.to_csv(file_path)
            print(f"{stock_name} data has been save at '{file_path}' location.")  
        else:
            raise TypeError("Only String are allowed")
    
    def __load_stock_data(self, stock_name: str) -> pd.DataFrame:
        """
        The function `__load_stock_data` downloads stock data if not already downloaded and returns it
        as a pandas DataFrame.
        
        :param stock_name: The `stock_name` parameter is a string that represents the name of the stock
        for which you want to load the data
        :type stock_name: str
        :return: a pandas DataFrame containing stock data for the specified stock name within the
        specified date range and frequency. The data is loaded from a CSV file located at the file path
        generated based on the stock name, start date, end date, and frequency. If the CSV file does not
        exist, the function first downloads the data using the `__download_data` method before loading
        it into a DataFrame
        """
        TEMP_DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "download")
        if not os.path.exists(TEMP_DOWNLOAD_FOLDER):
            os.makedirs(TEMP_DOWNLOAD_FOLDER)

        formated_date1 = self.start_date.strftime("%Y%m%d")
        formated_date2 = self.end_date.strftime("%Y%m%d")
        filename = "".join(re.findall(r'[a-zA-Z]', stock_name))+\
        f"-{str(formated_date1)}-{str(formated_date2)}-{self.freq}.csv"
        file_path = os.path.join(TEMP_DOWNLOAD_FOLDER, filename)

        if not os.path.exists(file_path):
            self.__download_data(stock_name, file_path)
        
        return pd.read_csv(file_path)
    
    def create_stock(self, stock_name: str) -> Stock:
        """
        The function creates a stock object with the given stock name and loads its data.
        
        :param stock_name: The `stock_name` parameter is a string that represents the name of the stock
        for which you want to create a new `Stock` object
        :type stock_name: str
        :return: An instance of the Stock class with the stock name and loaded stock data.
        """
        return Stock(stock_name, self.__load_stock_data(stock_name))
