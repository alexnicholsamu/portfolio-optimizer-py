import data_collection

symbols= ["AAP", "STZ", "COST", "DG", "DPZ", "EL", "LULU", "LVMUY", "TGT", "ARES", "BAC", "BRK-B",
               "CI", "V", "BMY", "CVS", "DHR", "ELV", "ISRG", "SNY", "VEEV", "VRTX", "AGCO", "BLDR",
               "CP", "DAC", "DAL", "LMT", "ROP", "SNA", "WM", "APD", "ETN", "FMC", "MP", "NEE", "RIO", "SEDG", "GOOGL", "GOOG",
               "AAPL", "MTCH", "NVDA", "PYPL", "CRM", "SHOP", "VZ", "VIVHY"]

data_batch = {"Risk Free Rate": 0.035,  # 10 year treasury bond return
                "Number of Iterations": 100,  # Number of times to disturb market for sensitivity checks
                "Volatility": "Low",  # High or Low
                "Return Perturbation": 0.05,  # Perturbations of Market
                "Total Portfolio Value": 1250000}

if __name__ == "__main__":
    print(data_collection.collect_data(symbols, data_batch))
    