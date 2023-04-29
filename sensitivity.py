import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns


def sensitivityAnalysis(price_data, num_iterations, volatility):
    results = []
    for i in range(num_iterations):
        weights, performance = optimize_portfolio(price_data, volatility)
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


def optimize_portfolio(price_data, volatility):
    mu = expected_returns.mean_historical_return(price_data)
    S = risk_models.sample_cov(price_data)

    ef = EfficientFrontier(mu, S)
    if volatility == "Minimum":
        raw_weights = ef.min_volatility()
    else:
        raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    performance = ef.portfolio_performance()

    return cleaned_weights, performance
