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

    async def calculate(self):
        rors = await self._common.calculate_rate_of_returns(self._assets, [12])
        if any(not rors[ticker] or rors[ticker].get(12) is None for ticker in self._assets):
            print("Warning: Missing data for one or more tickers. Stopped.")
            return []

        spy_ror = rors["SPY"][12]
        iefa_ror = rors["IEFA"][12]
        bil_ror = rors["BIL"][12]

        if spy_ror > bil_ror:
            return ["SPY" if spy_ror >= iefa_ror else "IEFA"]
        else:
            return await self._daa.calculate()
