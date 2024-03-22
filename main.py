import datetime as dt

from utils.stock import StockFactory
from utils.metrics import Performance
from utils.portfolio import PortfolioFactory
from utils.benchmark import BenchmarkFactory


if __name__ == "__main__":
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(4000)
    freq1 = "1d"

    stock_factory = StockFactory(start_date, end_date, freq1)
    stock = stock_factory.create_stock("TCS.NS")

    benchmark_factory = BenchmarkFactory(start_date, end_date, freq1)
    benchmark = benchmark_factory.create_benchmark(["^NSEI", "^BSESN"])

    portfolio_factory = PortfolioFactory(start_date, end_date, freq1)
    portfolio = portfolio_factory.create_portfolio(
        ["TCS.NS", "RELIANCE.NS", "MRF.NS"], 
        (0.3, 0.4, 0.3)
    )

    print(f"============ Performance ============")
    metric = Performance(portfolio, benchmark)
    print(metric)
    print(metric.get_all_metric(0.05))
    metric.visualize_return()

    metric = Performance(stock, benchmark)
    print(metric)
    print(metric.get_all_metric(0.05))
    metric.visualize_return()
