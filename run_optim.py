import ticker_select

symbols_all = ["AAP", "STZ", "COST", "DG", "DPZ", "EL", "LULU", "LVMUY", "TGT", "ARES", "BAC", "BRK-B",
               "CI", "V", "BMY", "CVS", "DHR", "ELV", "ISRG", "SNY", "VEEV", "VRTX", "AGCO", "BLDR",
               "CP", "DAC", "DAL", "LMT", "ROP", "SNA", "WM", "APD", "ETN", "FMC", "MP", "NEE", "RIO", "SEDG", "GOOGL", "GOOG",
               "AAPL", "MTCH", "NVDA", "PYPL", "CRM", "SHOP", "VZ", "VIVHY"]

symbols_HC = ["BMY", "CVS", "DHR", "ELV", "ISRG", "SNY", "VEEV", "VRTX"]

total_portfolio_value = 1250000
data_batch = {"Risk Free Rate": 0.035, 
                "Number of Iterations": 100, 
                "Risk Free Rate Pertubation": 0.01, 
                "Beta Perturbation": 0.1, 
                "Standard Deviation Perturbation": 0.1}

if __name__ == "__main__":
    portfolio = ticker_select.collect_data(symbols_all, data_batch, total_portfolio_value)
    print(portfolio["Performance"])
    print(portfolio["Ticker Weights"])
    print("\nDiscrete allocation:")
    print(portfolio["Discrete Allocation"]["Discrete allocation: "])
    print("\nFunds remaining: $" + str(portfolio["Discrete Allocation"]["Funds remaining"]))
    print("\nSensitivity Average:")
    print(portfolio["Sensitivity Average"])
    print("\nDifference between optimized and sensitivity average:")
    print(portfolio["Sensitivity Difference"])
    print("\nSensitivity Standard Deviation:")
    print(portfolio["Sensitivity Standard Deviation"])