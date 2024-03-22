import numpy as np
import pandas as pd
import datetime as dt
from typing import Optional, Union

from .stock import StockFactory
from .icomponent import IComponent

# Benchmark object is typically a collection of stocks that serves as a standard against which the performance 
# of individual stocks, mutual funds, and investment portfolios can be measured.
# This class represents a benchmark stock and implements the IComponent interface.
class Benchmark(IComponent):
    def __init__(
            self, 
            stocks: Union[list[IComponent], tuple[IComponent]]
        ) -> None:
        """
        This Python function initializes an object with a list or tuple of IComponent objects as a parameter.
        
        :param stocks: The `stocks` parameter in the `__init__` method is expected to be a list or tuple
        containing instances of the `IComponent` class. This parameter is used to initialize the `stocks`
        attribute of the class instance
        :type stocks: Union[list[IComponent], tuple[IComponent]]
        """
        self.stocks = stocks
    
    def __repr__(self) -> str:
        """
        The function `__repr__` returns a string representation of a `Benchmark` object by concatenating
        the names of stocks in the benchmark.
        :return: The `__repr__` method is returning a string representation of the `Benchmark` object,
        including the names of the stocks in the benchmark.
        """
        st = "Benchmark["
        for stock in self.stocks:
            st+=stock.name+","
        st=st[:-1]+"]"
        return st
    
    def get_stocks(self) -> Union[list[IComponent], tuple[IComponent]]:
        """
        The function `get_stocks` returns a list or tuple of IComponent objects.
        :return: A list of IComponent objects or a tuple containing a single IComponent object.
        """
        return self.stocks
    
    def get_stock(self, name: str) ->  Optional[IComponent]:
        """
        This method is used to retrieve a stock from the list of stocks by its name.
        Parameters:
        name (str): The name of the stock to retrieve.
        Returns:
        Optional[IComponent]: Returns the IComponent object if found, else returns None.
        """
        for stock in self.stocks:
            if(stock.name == name):
                return stock
        return None
    
    def get_stocks_name(self) -> list[str]:
        """
        This method is used to retrieve the names of all the stocks in the list.
        Returns:
        list[str]: Returns a list of names of all the stocks.
        """
        return [stock.name for stock in self.stocks]
    
    def get_total_stocks(self) -> int:
        """
        This method is used to get the total number of stocks in the list.
        Returns:
        int: Returns the total number of stocks.
        """
        return len(self.stocks)
    
    def get_daily_return(self) -> pd.DataFrame:
        """
        This method is used to get the daily return of each stock in the list.
        Returns:
        pd.DataFrame: Returns a pandas DataFrame where each column represents a stock and 
        each row represents the daily return of that stock.
        """
        stock_returns_lst = [stock.get_daily_return() for stock in self.stocks]
        # The `stock_returns_lst = pd.concat(stock_returns_lst, axis=1)` line of code is using the 
        # concat function from the pandas library in Python to concatenate (join) a list of pandas 
        # DataFrame objects stored in stock_returns_lst along the columns axis (axis=1).
        stock_returns_lst = pd.concat(stock_returns_lst, axis=1)
        stock_returns_lst.columns = [stock.name for stock in self.stocks]
        return stock_returns_lst
    
    def get_cagr(self) -> np.ndarray:
        """
        This method is used to get the Compound Annual Growth Rate (CAGR) of each stock in the list.    
        Returns:
        np.ndarray: Returns a numpy array where each element represents the CAGR of a stock.
        """
        return np.array([stock.get_cagr() for stock in self.stocks])
    
    def get_std(self) -> np.ndarray:
        """
        This method is used to get the standard deviation of the returns of each stock in the list.
        Returns:
        np.ndarray: Returns a numpy array where each element represents the standard deviation of 
        the returns of a stock.
        """
        return np.array([stock.get_std() for stock in self.stocks])
    


# The `BenchmarkFactory` class is used to create `Benchmark` objects.
class BenchmarkFactory:
    def __init__(self, start_date: dt.datetime, end_date: dt.datetime, freq: str) -> None:
        """
        This is the constructor method for the BenchmarkFactory class. 
        It initializes a BenchmarkFactory object with a StockFactory object.
        Parameters:
        start_date (dt.datetime): The start date for the stock data.
        end_date (dt.datetime): The end date for the stock data.
        freq (str): The frequency of the stock data. This could be 'daily', 'weekly', 'monthly', etc.
        Returns:
        None
        """
        self.stock_factory = StockFactory(start_date, end_date, freq)
    
    def __create_stock(self, stock_name: str) -> IComponent:
        """
        This is a private method that uses the StockFactory object to create a IComponent object given 
        a stock name.
        Parameters:
        stock_name (str): The name of the stock to create.
        Returns:
        IComponent: Returns a IComponent object.
        """
        return self.stock_factory.create_stock(stock_name)
    
    def create_benchmark(self, stocks: Union[list[str], tuple[str]]) -> Benchmark:
        """
        This method creates a Benchmark object. It takes a list or tuple of stock names, 
        creates a IComponent object for each stock name using the __create_stock method, and then creates a 
        Benchmark object with the list of IComponent objects.
        Parameters:
        stocks (Union[list[str], tuple[str]]): A list or tuple of stock names.
        Returns:
        Benchmark: Returns a Benchmark object.
        """
        stocks_lst = [self.__create_stock(stock) for stock in stocks]
        return Benchmark(stocks=stocks_lst)
    