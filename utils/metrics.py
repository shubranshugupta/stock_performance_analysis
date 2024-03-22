import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .stock import Stock
from .icomponent import IComponent

# The Performance class in the selected code is used to calculate and store various performance 
# metrics of a stock or a portfolio of stocks against a benchmark.
class Performance:
    """
    This class is used to calculate and store various performance metrics of a stock or a 
    portfolio of stocks against a benchmark.
    Attributes:
    stocks (IComponent): A IComponent object.
    benchmarks (IComponent): A IComponent object.
    performace (dict): A dictionary to store the performance metrics.
    """
    def __init__(self, stocks: IComponent, benchmarks: IComponent) -> None:
        """
        Initializes the Performance object with a IComponent object, and a Benchmark object.
        Parameters:
        stocks (IComponent): A IComponent object.
        benchmarks (IComponent): A IComponent object.
        Returns:
        None
        """
        self.stocks = stocks
        self.benchmarks = benchmarks
        self.performace = {}

    def __repr__(self) -> str:
        """
        Returns a string representation of the Performance object.
        Returns:
        str: A string representation of the Performance object.
        """
        return f"Performance of {self.stocks.__repr__()} with {self.benchmarks.__repr__()}."

    def get_beta(self) -> np.ndarray:
        """
        Calculates and returns the beta of the stock or portfolio. Beta is a measure of the volatility, or 
        systematic risk, of a security or portfolio in comparison to the market as a whole.
        Returns:
        np.ndarray: A numpy array where each element represents the beta of a stock.
        """
        if "beta" not in self.performace:
            benchmark_return = self.benchmarks.get_daily_return()
            stock_return = self.stocks.get_daily_return()
            # `[benchmark_return[col].cov(stock_return) for col in benchmark_return.columns]`: This is a 
            # list comprehension that iterates over each column in the `benchmark_return` DataFrame. For 
            # each column, it calculates the covariance between the column (which represents the return 
            # of the benchmark) and `stock_return` (which represents the return of a stock). The `cov` method 
            # is a pandas DataFrame method that calculates the covariance between two series.
            coveriance = np.array([benchmark_return[col].cov(stock_return) for col in benchmark_return.columns])
            # `benchmark_return.var()`: This is calling the `var` method on the `benchmark_return` DataFrame. 
            # The `var` method calculates the variance of each column in the DataFrame. In this case, it 
            # calculates the variance of the returns of the benchmark.
            # `to_numpy()`: This is a method that converts the result (which is a pandas Series) to a numpy array.
            variance = benchmark_return.var().to_numpy()
            
            self.performace["beta"]=coveriance/variance
        
        return self.performace["beta"]

    def get_alpha(self, risk_free_return: float) -> np.ndarray:
        """
        Calculates and returns the alpha of the stock or portfolio. Alpha is a measure of the active 
        return on an investment, the performance of that investment compared with a suitable market 
        index.
        Parameters:
        risk_free_return (float): The risk-free rate of return.
        Returns:
        np.ndarray: A numpy array where each element represents the alpha of a stock.
        """
        if "alpha" not in self.performace:
            benchmark_return = self.benchmarks.get_cagr()
            stock_return = self.stocks.get_cagr()
            beta = self.get_beta()

            alpha = []
            for idx in range(beta.size):
                # The alpha is calculated as the difference between the stock's return and 
                # the risk-free return, minus the product of the stock's beta and the benchmark's 
                # return. The `idx` variable is used to index the `beta` and `benchmark_return` arrays 
                # to get the beta and return for each benchmark.
                alpha.append(stock_return-risk_free_return-(beta[idx]*benchmark_return[idx]))
            self.performace["alpha"]=np.array(alpha)

        return self.performace["alpha"]

    def get_return(self) -> np.ndarray:
        """
        Calculates and returns the return of the stock or portfolio compared to the benchmark.
        Returns:
        np.ndarray: A numpy array where each element represents the return of a stock.
        """
        if "return" not in self.performace:
            benchmark_return = self.benchmarks.get_cagr()
            stock_return = self.stocks.get_cagr()
            self.performace["return"] = stock_return/benchmark_return

        return self.performace["return"]

    def get_tracking_error(self) -> np.ndarray:
        """
        Calculates and returns the tracking error of the stock or portfolio. Tracking error is 
        a measure of how closely a portfolio follows the index to which it is benchmarked.
        Returns:
        np.ndarray: A numpy array where each element represents the tracking error of a stock.
        """
        if "tracking_error" not in self.performace:
            benchmark_return = self.benchmarks.get_daily_return()
            stock_return = self.stocks.get_daily_return()
            # `stock_return.sub(benchmark_return[col])`: This line subtracts the return of the benchmark 
            # from the return of the stock for each column in the `benchmark_return` DataFrame using `sub` 
            # method. `.std()``: This method calculates the standard deviation of the resulting series.
            self.performace["tracking_error"] = np.array([
                stock_return.sub(benchmark_return[col]).std() for col in benchmark_return.columns
            ])

        return self.performace["tracking_error"]

    def get_treynor_ratio(self, risk_free_return: float) -> np.ndarray:
        """
        Calculates and returns the Treynor Ratio of the stock or portfolio. The Treynor Ratio is a 
        performance metric for determining how well an investment has compensated its investors 
        given its level of risk.
        Parameters:
        risk_free_return (float): The risk-free rate of return.
        Returns:
        np.ndarray: A numpy array where each element represents the Treynor Ratio of a stock.
        """
        if "treynor_ratio" not in self.performace:
            stock_return = self.stocks.get_cagr()
            beta = self.get_beta()
            self.performace["treynor_ratio"] = (stock_return-risk_free_return)/beta

        return self.performace["treynor_ratio"]

    def get_sharpe_ratio(self, risk_free_return: float) -> np.ndarray:
        """
        Calculates and returns the Sharpe Ratio of the stock or portfolio. The Sharpe Ratio is a 
        measure of risk-adjusted return.
        Parameters:
        risk_free_return (float): The risk-free rate of return.
        Returns:
        np.ndarray: A numpy array where each element represents the Sharpe Ratio of a stock.
        """
        if "sharpe_ratio" not in self.performace:
            stock_std = self.stocks.get_std()
            stock_cagr = self.stocks.get_cagr()
            self.performace["sharpe_ratio"] = (stock_cagr-risk_free_return)/stock_std

        return self.performace["sharpe_ratio"]

    def get_all_metric(self, risk_free_return) -> pd.DataFrame:
        """
        Calculates all the above metrics and returns them in a pandas DataFrame.
        Parameters:
        risk_free_return (float): The risk-free rate of return.
        Returns:
        pd.DataFrame: A pandas DataFrame where each column represents a performance metric 
        and each row represents a stock.
        """
        self.get_beta()
        self.get_alpha(risk_free_return)
        self.get_return()
        self.get_tracking_error()
        self.get_treynor_ratio(risk_free_return)
        self.get_sharpe_ratio(risk_free_return)

        return pd.DataFrame(self.performace, index=self.benchmarks.get_daily_return().columns)

    def visualize_return(self):
        """
        Plots the cumulative daily return of the stock or portfolio and the benchmark.
        Returns:
        None
        """
        stock_return = (self.stocks.get_daily_return()+1).sort_index().cumsum()
        if(type(self.stocks)==Stock):
            stock_return.name = self.stocks.name
        else:
            stock_return.name = "Portfolio"
        benchmark_return = (self.benchmarks.get_daily_return()+1).sort_index().cumsum()
        returns = benchmark_return.join(stock_return)

        returns.plot()
        plt.legend()
        plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
        plt.show()