import pandas as pd
import yfinance as yf
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import numpy as np
from datetime import date, timedelta

# add a difference calculator between sensitivity average and normal allocation

symbols_all = ["AAP", "STZ", "COST", "DG", "DPZ", "EL", "LULU", "LVMUY", "TGT", "ARES", "BAC", "BRK-B",
               "CI", "V", "BMY", "CVS", "DHR", "ELV", "ISRG", "SNY", "VEEV", "VRTX", "AGCO", "BLDR",
               "CP", "DAC", "DAL", "LMT", "ROP", "SNA", "WM", "APD", "ETN", "FMC", "MP", "NEE", "RIO", "SEDG", "GOOGL", "GOOG",
               "AAPL", "MTCH", "NVDA", "PYPL", "CRM", "SHOP", "VZ", "VIVHY"]

symbols_HC = ["BMY", "CVS", "DHR", "ELV", "ISRG", "SNY", "VEEV", "VRTX"]


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


def getPerformance(price_data, risk_free_rate):
    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(price_data)
    s = risk_models.sample_cov(price_data)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, s)
    raw_weights = ef.max_sharpe(risk_free_rate=risk_free_rate)
    cleaned_weights = ef.clean_weights()
    return cleaned_weights, ef.portfolio_performance(verbose=True, risk_free_rate=risk_free_rate)  # verbose is why it prints


def discreteAllocation(price_data, cleaned_weights, portfolio_value):
    latest_prices = get_latest_prices(price_data)
    weights = cleaned_weights

    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=portfolio_value)
    allocation, leftover = da.greedy_portfolio()
    return {"Discrete allocation: ": allocation,
            "Funds remaining: $": round(leftover, 2)}


def optimize_portfolio(price_data, risk_free_rate, beta, std_dev, weight_bounds=(0, 1)):
    mu = expected_returns.mean_historical_return(price_data)
    S = risk_models.sample_cov(price_data)

    # Adjust expected returns and covariance matrix based on the input beta and standard deviation
    adjusted_mu = mu * beta
    adjusted_S = S * std_dev

    ef = EfficientFrontier(adjusted_mu, adjusted_S, weight_bounds)
    raw_weights = ef.max_sharpe(risk_free_rate=risk_free_rate)
    cleaned_weights = ef.clean_weights()
    performance = ef.portfolio_performance(verbose=False, risk_free_rate=risk_free_rate)

    return cleaned_weights, performance


def sensitivityAnalysis(price_data, risk_free_rate, num_iterations=100,
                        risk_free_rate_perturbation=0.01, beta_perturbation=0.1, std_dev_perturbation=0.1):
    results = []
    for i in range(num_iterations):
        perturbed_risk_free_rate = risk_free_rate * (1 + np.random.normal(0, risk_free_rate_perturbation))
        perturbed_beta = 1 * (1 + np.random.normal(0, beta_perturbation))
        perturbed_std_dev = 1 * (1 + np.random.normal(0, std_dev_perturbation))

        weights, performance = optimize_portfolio(price_data, perturbed_risk_free_rate, perturbed_beta, perturbed_std_dev)
        results.append(weights)

    average_weights = pd.DataFrame(results).mean()
    std_weights = pd.DataFrame(results).std()
    sensitivity_average = {}
    sensitivity_std = {}
    for symbol, average_weight in average_weights.items():
        if not average_weight == 0.000000:
            sensitivity_average[symbol] = round(average_weight, 4)
    for symbol, std_weight in std_weights.items():
        if not std_weight == 0.000000:
            sensitivity_std[symbol] = round(std_weight, 4)
    return sensitivity_average, sensitivity_std


def getSensitivityDifference(weights, sensitivity_average):
    ticker_list = sensitivity_average.keys()
    list_diff = {}
    for symbol, value in weights.items():
        if symbol in ticker_list:
            list_diff[symbol] = round(sensitivity_average.get(symbol) - value, 6)
    return list_diff


if __name__ == "__main__":
    ticker_data = downloadData(symbols_all)
    risk_free_weight = 0.035
    total_portfolio_value = 1250000
    ticker_weights, performance = getPerformance(ticker_data, risk_free_weight)
    sens_average, sens_std = sensitivityAnalysis(ticker_data, risk_free_weight)
    sensitivity_diff = getSensitivityDifference(ticker_weights, sens_average)
    discrete_allocation = discreteAllocation(ticker_data, ticker_weights, total_portfolio_value)
    print(ticker_weights)
    print("\nDiscrete allocation:")
    print(discrete_allocation["Discrete allocation: "])
    print("\nFunds remaining: $" + str(discrete_allocation["Funds remaining: $"]))
    print("\nSensitivity Average:")
    print(sens_average)
    print("\nDifference between optimized and sensitivity average:")
    print(sensitivity_diff)
    print("\nSensitivity Standard Deviation:")
    print(sens_std)
