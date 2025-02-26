# Adaptive Dual Momentum Strategy

class ADM:
    def __init__(self, common, daa):
        self._common = common
        self._daa = daa
        self._assets = [
            "SPY",  # SPDR S&P 500 | US Stocks
            "IEFA",  # iShares Core MSCI EAFE : Developed Market Stocks
            "BIL",  # SPDR Bloomberg Barclay 1-3 Month T-Bill : Cash
        ]

    def calculate(self):
        rors = self._common.calculate_rate_of_returns(self._assets, 12)
        if any(rors[ticker] is None for ticker in self._assets):
            print("Warning: Missing data for one or more tickers. Stopped.")
            return []

        spy_ror = rors["SPY"]
        iefa_ror = rors["IEFA"]
        bil_ror = rors["BIL"]

        return [max("SPY", "IEFA", key=lambda x: rors[x])] if spy_ror > bil_ror else self._daa.calculate()
