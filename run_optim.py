import data_collection

symbols_all = ["AAP", "STZ", "COST", "DG", "DPZ", "EL", "LULU", "LVMUY", "TGT", "ARES", "BAC", "BRK-B",
               "CI", "V", "BMY", "CVS", "DHR", "ELV", "ISRG", "SNY", "VEEV", "VRTX", "AGCO", "BLDR",
               "CP", "DAC", "DAL", "LMT", "ROP", "SNA", "WM", "APD", "ETN", "FMC", "MP", "NEE", "RIO", "SEDG", "GOOGL", "GOOG",
               "AAPL", "MTCH", "NVDA", "PYPL", "CRM", "SHOP", "VZ", "VIVHY"]

symbols_HC = ["BMY", "CVS", "DHR", "ELV", "ISRG", "SNY", "VEEV", "VRTX"]

data_batch = {"Risk Free Rate": 0.035,  # 10 year treasury bond return
                "Number of Iterations": 10, 
                "Volatility": "Minimum",  # Minimum or Maximum
                "Total Portfolio Value": 1250000}

if __name__ == "__main__":
    portfolio = data_collection.collect_data(symbols_all, data_batch)
    print("\nReturn on Assets:")
    print(f"{(portfolio['Performance'][0]*100):.2f}%")
    print("Volatility:")
    print(f"{(portfolio['Performance'][1]*100):.2f}%")
    print("Sharpe Ratio:")
    print(f"{(portfolio['Performance'][2]):.2f}%\n")
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