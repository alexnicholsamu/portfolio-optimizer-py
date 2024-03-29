import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns


def sensitivityAnalysis(price_data, num_iterations, volatility, used_tickers, return_perturbation):
    """
    Collects optimized portfolio data for a disturbed market, to check sensitivity of the optimized portfolio
    """
    results = []
    for i in range(num_iterations):
        weights, performance = optimize_portfolio(price_data, volatility, return_perturbation)
        results.append(weights)
    average_weights = pd.DataFrame(results).mean()
    std_weights = pd.DataFrame(results).std()
    return getSensitivityData(average_weights, std_weights, used_tickers)


def getSensitivityData(average, std, tickers):
    """
    Organizes data to be returned, making sure there isn't any unnecessary information
    """
    sensitivity_average = {}
    sensitivity_std = {}
    ticker_list = [ticker for ticker, value in tickers.items() if value != 0.0]
    for symbol, average_weight in average.items():
        if symbol in ticker_list:
            sensitivity_average[symbol] = round(average_weight, 4)
    for symbol, std_weight in std.items():
        if symbol in ticker_list:
            sensitivity_std[symbol] = round(std_weight, 4)
    return sensitivity_average, sensitivity_std


def getSensitivityDifference(weights, sensitivity_average):
    """
    Calculates the difference between the optimized portfolio and the disturbed portfolio
    """
    ticker_list = sensitivity_average.keys()
    list_diff = {}
    for symbol, value in weights.items():
        if symbol in ticker_list:
            list_diff[symbol] = round(sensitivity_average.get(symbol) - value, 6)
    return list_diff


def optimize_portfolio(price_data, volatility, return_perturbation):
    """
    Optimizes portfolio of disturbed market
    """
    mu = expected_returns.mean_historical_return(price_data)
    S = risk_models.sample_cov(price_data)
    perturbed_mu = mu * (1 + np.random.normal(0, return_perturbation))

    ef = EfficientFrontier(perturbed_mu, S)
    if volatility == "Low":
        raw_weights = ef.min_volatility()
    else:
        raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    performance = ef.portfolio_performance()

    return cleaned_weights, performance
