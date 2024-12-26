# Adaptive Dual Momentum Strategy

class ADM:
    def __init__(self, common, daa):
        self._common = common
        self._daa = daa

    def calculate(self):
        spy_ror = self._calculate_rate_of_return("SPY")    # SPDR S&P 500 | US Stocks
        efa_ror = self._calculate_rate_of_return("EFA")    # iShares MSCI EAFE : Developed Market Stocks
        bil_ror = self._calculate_rate_of_return("BIL")    # SPDR Bloomberg Barclay 1-3 Month T-Bill : Cash

        if spy_ror > bil_ror:
            if spy_ror >= efa_ror:
                return ["SPY"]
            else:
                return ["EFA"]
        else:
            return self._daa.calculate()

    def _calculate_rate_of_return(self, ticker):
        return self._common.calculate_rate_of_return(ticker, 12)
