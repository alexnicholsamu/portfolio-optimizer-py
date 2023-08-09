import pandas as pd
import yfinance as yf
import sensitivity
import optimize
from datetime import date, timedelta


def getTreasuryReturn():
    data = yf.download('^TNX', period='1d')
    ten_year_treasury_rate = data['Close'][0]
    return ten_year_treasury_rate


def getNames(data):
    """
    Replaces ticker name with company name
    """
    returnString = ""
    for ticker, value in data:
        name = yf.Ticker(ticker)
        longname = name.info['longName']
        returnString = returnString + f"{longname}: {value}\n"
    return returnString


def downloadData(tickers):
    """
    Gathers and organizes closing prices in the past 10 years for stocks
    """
    start_date = date.today() - timedelta(days=3650)
    end_date = date.today() - timedelta(days=1)
    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', progress=False)
    price_data = pd.DataFrame()
    for ticker in tickers:
        if ticker in data:
            price_data[ticker] = data[ticker]['Close']
    price_data = price_data.dropna(axis=1)
    return price_data


def collect_data(symbols, data_batch):
    """
    Master method, gathers all data into one spot and formats output
    """
    data_batch = data_batch
    ticker_data = downloadData(symbols)
    ticker_weights, performance = optimize.getPerformance(ticker_data, data_batch["Risk Free Rate"], data_batch["Volatility"])
    sens_average, sens_std = sensitivity.sensitivityAnalysis(ticker_data, data_batch["Number of Iterations"], data_batch["Volatility"], ticker_weights, data_batch["Return Perturbation"])
    sensitivity_diff = sensitivity.getSensitivityDifference(ticker_weights, sens_average)
    discrete_allocation = optimize.discreteAllocation(ticker_data, ticker_weights, data_batch["Total Portfolio Value"])
    retstring = f"\nReturn on Assets:\n{(performance[0]*100):.2f}%\n" 
    retstring += f"Volatility:\n{(performance[1]*100):.2f}%\n"
    retstring += f"Sharpe Ratio: \n{(performance[2]):.2f}%\n"
    retstring += f"\nWeighted Portfolio: \n{getNames(ticker_weights.items())}\n"
    retstring += f"Discrete allocation: \n{getNames(discrete_allocation['Discrete allocation: '].items())}\n"
    retstring += f"Funds remaining: \n${str(discrete_allocation['Funds remaining'])}\n"
    retstring += f"\nSensitivity Average: \n{getNames(sens_average.items())}\n"
    retstring += f"Difference between optimized and sensitivity average: \n{getNames(sensitivity_diff.items())}\n"
    retstring += f"Sensitivity Standard Deviation: \n{getNames(sens_std.items())}"
    return retstring
