import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns

def sensitivityAnalysis(price_data, data_batch):
    risk_free_rate, num_iterations, risk_free_rate_perturbation, beta_perturbation, std_dev_perturbation = data_batch.values()
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