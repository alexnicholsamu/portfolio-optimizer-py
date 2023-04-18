from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


def getPerformance(price_data, risk_free_rate):
    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(price_data)
    s = risk_models.sample_cov(price_data)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, s)
    raw_weights = ef.max_sharpe(risk_free_rate=risk_free_rate)
    cleaned_weights = ef.clean_weights()
    return cleaned_weights, ef.portfolio_performance(risk_free_rate=risk_free_rate)  # verbose is why it prints


def discreteAllocation(price_data, cleaned_weights, portfolio_value):
    latest_prices = get_latest_prices(price_data)
    weights = cleaned_weights

    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=portfolio_value)
    allocation, leftover = da.greedy_portfolio()
    return {"Discrete allocation: ": allocation,
            "Funds remaining": round(leftover, 2)}