import numpy as np
import pandas as pd
import datetime as dt
from typing import Optional, Union

from .stock import StockFactory
from .icomponent import IComponent

# The `Portfolio` class represents a collection of stocks with methods to calculate daily return,
# compound annual growth rate (CAGR), and standard deviation.
# This class represents a portfolio and implements the IComponent interface.
class PortFolio(IComponent):
    def __init__(
            self, 
            stocks: Union[list[IComponent], tuple[IComponent]], 
            weights: Union[list[float], tuple[float]]
        ) -> None:
        """
        This Python function initializes an object with a list or tuple of IComponent objects and
        corresponding weights.
        :param stocks: The `stocks` parameter is expected to be a list or tuple containing instances of
        the `IComponent` class
        :type stocks: Union[list[IComponent], tuple[IComponent]]
        :param weights: The `weights` parameter is expected to be a list or tuple of floats representing
        the weights assigned to each stock in the `stocks` parameter. Each weight corresponds to a stock
        in the `IComponent` list or tuple
        :type weights: Union[list[float], tuple[float]]
        """
        self.stocks = stocks
        self.weights = weights
    
    def __repr__(self) -> str:
        """
        The `__repr__` function returns a string representation of a Portfolio object by concatenating
        the names of the stocks it contains.
        :return: The `__repr__` method is returning a string representation of the `Portfolio` object.
        It concatenates the names of all the stocks in the portfolio separated by commas within square
        brackets. For example, if the portfolio contains stocks with names "AAPL", "GOOGL", and "MSFT",
        the returned string would be "Portfolio[AAPL,GOOGL,MSFT]
        """
        st = "Portfolio["
        for stock in self.stocks:
            st+=stock.name+","
        st=st[:-1]+"]"
        return st
    
    def get_stocks(self) -> Union[list[IComponent], tuple[IComponent]]:
        """
        The function `get_stocks` returns a list or tuple of IComponent objects.
        :return: The method `get_stocks` is returning either a list of `IComponent` objects or a tuple
        containing a single `IComponent` object.
        """
        return self.stocks
    
    def get_stock(self, name: str) ->  Optional[IComponent]:
        """
        This function searches for a stock by name in a list of stocks and returns the stock if found,
        otherwise returns None.
        
        :param name: The `name` parameter in the `get_stock` method is a string that represents the name
        of the stock that you want to retrieve from the list of stocks stored in the object. The method
        iterates through the list of stocks and returns the stock object that matches the provided name.
        If no stock
        :type name: str
        :return: The `get_stock` method is returning an instance of the `IComponent` class if a stock with
        the specified name is found in the list of stocks. If no stock with the specified name is found,
        it returns `None`.
        """
        for stock in self.stocks:
            if(stock.name == name):
                return stock
        return None
    
    def get_total_stocks(self) -> int:
        """
        The function `get_total_stocks` returns the total number of stocks in a given object.
        :return: The `get_total_stocks` method is returning the total number of stocks in the
        `self.stocks` list as an integer.
        """
        return len(self.stocks)
    
    def get_daily_return(self) -> pd.Series:
        """
        The function `get_daily_return` calculates the weighted sum of daily returns for a portfolio of
        stocks.
        :return: The `get_daily_return` method returns a pandas Series that represents the weighted sum
        of daily returns for a portfolio of stocks.
        """
        # The line `stock_returns_lst = [stock.get_daily_return() for stock in self.stocks]` is
        # creating a list called `stock_returns_lst` by iterating over each stock in the `self.stocks`
        # list and calling the `get_daily_return()` method on each stock.
        stock_returns_lst = [stock.get_daily_return() for stock in self.stocks]
        # The line `return pd.concat(stock_returns_lst, axis=1).mul(self.weights).sum(axis=1)` in the
        # `get_daily_return` method of the `Portfolio` class is performing the following operations:
        # 1. Concat all the Series in the `stock_returns_lst` list columnwise.
        # 2. Multiply the list of weight with the `DataFrame` columnwise.
        # 3. Sum of all the column and return `Series`.
        return pd.concat(stock_returns_lst, axis=1).mul(self.weights).sum(axis=1)
    
    def get_cagr(self) -> np.float64:
        """
        The function calculates the Compound Annual Growth Rate (CAGR) for a portfolio of stocks by
        multiplying each stock's CAGR with its corresponding weight and summing the results.
        :return: The `get_cagr` method is returning the Compound Annual Growth Rate (CAGR) for a
        portfolio of stocks. It calculates this by multiplying each stock's CAGR with its corresponding
        weight, then summing up all the values in the resulting array.
        """
        # The line `stock_returns_lst = np.array([stock.get_cagr() for stock in self.stocks])` is
        # creating a NumPy array by iterating over each stock in the `self.stocks` list and calling
        # the `get_cagr()` method on each stock. This results in an array containing the compound
        # annual growth rate (CAGR) values of each stock in the portfolio.
        stock_returns_lst = np.array([stock.get_cagr() for stock in self.stocks])
        # The line `return np.sum(stock_returns_lst*np.array(self.weights))` in the `get_cagr` method
        # of the `Portfolio` class is calculating the Compound Annual Growth Rate (CAGR) for a
        # portfolio of stocks. Here's a breakdown of what it's doing:
        # 1. Multiply Each stock CAGR with corresponding weight Example [1, 2, 3]*[1, 2, 3] = [1, 4, 9]
        # 2. Sum of all the values in the `np.array` Example [1, 4, 9] = 14
        return np.sum(stock_returns_lst*np.array(self.weights))
    
    def get_std(self) -> float:
        """
        The function `get_std` calculates the standard deviation of daily returns.
        :return: The code snippet is defining a method named `get_std` that calculates the standard
        deviation of daily returns. The method calls another method `get_daily_return()` to get the
        daily returns and then calculates the standard deviation using the `std()` method. The method
        returns the calculated standard deviation as a float value.
        """
        return self.get_daily_return().std()


# The `PortfolioFactory` class creates a portfolio by generating individual stocks using a specified
# start date, end date, and frequency, and assigning weights to each stock.
class PortfolioFactory:
    def __init__(self, start_date: dt.datetime, end_date: dt.datetime, freq: str) -> None:
        """
        The function initializes a StockFactory object with specified start date, end date, and
        frequency parameters.
        
        :param start_date: The `start_date` parameter is a datetime object representing the beginning
        date for a time period
        :type start_date: dt.datetime
        :param end_date: The `end_date` parameter represents the end date for a time period. It is a
        datetime object that specifies the date and time at which the period ends
        :type end_date: dt.datetime
        :param freq: The `freq` parameter in the `__init__` method is a string that represents the
        frequency of the stock data. It could be daily, weekly, monthly, etc., depending on how often
        you want the stock data to be sampled or updated
        :type freq: str
        """
        self.stock_factory = StockFactory(start_date, end_date, freq)

    
    def __create_stock(self, stock_name: str) -> IComponent:
        """
        This function creates a stock object using a stock factory based on the provided stock name.
        :param stock_name: The `stock_name` parameter is a string that represents the name of the stock
        that you want to create
        :type stock_name: str
        :return: An instance of the IComponent class is being returned.
        """
        return self.stock_factory.create_stock(stock_name)
    
    def create_portfolio(
            self, 
            stocks: Union[list[str], tuple[str]], 
            weights: Union[list[float], tuple[float]]
        ) -> PortFolio:
        """
        The function `create_portfolio` takes a list of stocks and their corresponding weights,
        validates the weights, creates stock objects, and returns a Portfolio object.
        
        :param stocks: The `stocks` parameter is a list or tuple of stock symbols (strings) that you
        want to include in the portfolio. Each stock symbol represents a specific stock that you want to
        invest in
        :type stocks: Union[list[str], tuple[str]]
        :param weights: The `weights` parameter in the `create_portfolio` function is expected to be a
        list or tuple of float values. These weights represent the proportion of each stock in the
        portfolio. The sum of all weights should be equal to 1, indicating the total allocation of the
        portfolio. Each weight corresponds to
        :type weights: Union[list[float], tuple[float]]
        :return: The `create_portfolio` method returns an instance of the `Portfolio` class with the
        provided list of stocks and their corresponding weights.
        """

        # The code snippet `if(len(stocks)!=len(weights)): raise Exception("Please provide weight for
        # all stocks")` is performing a validation check in the `create_portfolio` method of the
        # `PortfolioFactory` class.
        if(len(stocks)!=len(weights)):
            raise Exception("Please provide weight for all stocks")
        # The code snippet `if(sum(weights)!=1): raise Exception("Sum of all weight should be 1")` is
        # performing a validation check in the `create_portfolio` method of the `PortfolioFactory`
        # class.
        if(sum(weights)!=1):
            raise Exception("Sum of all weight should be 1")
        
        stocks_lst = [self.__create_stock(stock) for stock in stocks]
        return PortFolio(stocks=stocks_lst, weights=weights)
    
