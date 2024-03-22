# Stock Performance Analysis

This project provides a set of tools for analyzing the performance of stocks and portfolios against a benchmark.

## Features

- Calculate various performance metrics such as return, beta, alpha, tracking error, Treynor Ratio, and Sharpe Ratio.
- Visualize the cumulative daily return of a stock or portfolio and the benchmark.
- Create a benchmark from a list of stocks.
- Calculate the Compound Annual Growth Rate (CAGR) and the standard deviation of the returns of each stock in a benchmark.

## Classes

- `Stock`: Represents a stock. Can calculate its daily return, CAGR, and standard deviation of returns.
- `StockFactory`: Creates `Stock` objects.
- `Portfolio`: Represents a portfolio of stocks. Can calculate its daily return, CAGR, and standard deviation of returns.
- `PortfolioFactory`: Creates `Portfolio` objects.
- `Benchmark`: Represents a benchmark, which is a collection of stocks.
- `BenchmarkFactory`: Creates `Benchmark` objects.
- `Performance`: Calculates and stores various performance metrics of a stock or a portfolio of stocks against a benchmark.

## UML Class Diagram

![UML Class Diagram](image\portfolio_performance_uml_class_diagram.png)

## Usage

First, create a `Stock` object using `StockFactory` or `Portfolio` object using `PortfolioFactory` and also create `Benchmark` object using the `BenchmarkFactory` class. Then, create a `Performance` object with a `Stock` or `Portfolio` object and the `Benchmark` object. You can then use the methods of the `Performance` object to calculate various performance metrics and visualize the cumulative daily return.

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib

## Installation

Clone this repository and install the required packages:

```bash
git clone https://github.com/yourusername/stock-performance-analysis.git
cd stock-performance-analysis
pip install -r requirements.txt
```
