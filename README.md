# portfolio-optimizer-py, a portfolio optimizer by Alexander Nichols

## Tools used in the creation of this project:
 
> yfinance, PyPortfolioOpt

## Summary:

This is my portfolio optimizer, where with the input of stock tickers (represented by some example tickers in 'symbols'), and other optimization factors (current: Risk Free Rate, Number of Iterations, Volatility (High/Low), Return Perturbation) an investor could get the optimzied portfolio (in reference to the past 10 years) for their stocks. With the addition of a portfolio value integer, an investor can now use that information to get numerical values for the amount of shares to buy for each one of the recommended stocks. The Return Perturbations will perform sensitivity analysis on the Portfolio.

Future work includes more customized variables for optimization, other forms of optimization (not soley Sharpe Ratio)

All files are necessary to run this

License can be found in the [License](LICENSE.md), and any and all suggestions should be emailed to _alexander.k.nichols@gmail.com_
