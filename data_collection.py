import pandas as pd
import yfinance as yf
import sensitivity
import optimize
from datetime import date, timedelta


def downloadData(tickers):
    start_date = date.today() - timedelta(days=2920)
    end_date = date.today() - timedelta(days=1)
    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', progress=False)
    price_data = pd.DataFrame()
    for ticker in tickers:
        if ticker in data:
            price_data[ticker] = data[ticker]['Close']
    price_data = price_data.dropna(axis=1)
    return price_data


def collect_data(symbols, data_batch):
    data_batch = data_batch
    ticker_data = downloadData(symbols)
    ticker_weights, performance = optimize.getPerformance(ticker_data, data_batch["Risk Free Rate"], data_batch["Volatility"])
    sens_average, sens_std = sensitivity.sensitivityAnalysis(ticker_data, data_batch["Number of Iterations"], data_batch["Volatility"])
    sensitivity_diff = sensitivity.getSensitivityDifference(ticker_weights, sens_average)
    discrete_allocation = optimize.discreteAllocation(ticker_data, ticker_weights, data_batch["Total Portfolio Value"])
    return {"Performance": performance,
            "Ticker Weights": ticker_weights,
            "Sensitivity Average": sens_average,
            "Sensitivity Standard Deviation": sens_std,
            "Sensitivity Difference": sensitivity_diff,
            "Discrete Allocation": discrete_allocation}
    
