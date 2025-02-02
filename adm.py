# Adaptive Dual Momentum Strategy

class ADM:
    def __init__(self, common, daa):
        self._common = common
        self._daa = daa

    def calculate(self):
        spy_ror = self._calculate_rate_of_return("SPY")    # SPDR S&P 500 | US Stocks
        if spy_ror is None:
            print("Warning: No data for SPY. Stopped.")
            return []
        efa_ror = self._calculate_rate_of_return("IEFA")  # iShares Core MSCI EAFE : Developed Market Stocks
        if efa_ror is None:
            print("Warning: No data for IEFA. Stopped.")
            return []
        bil_ror = self._calculate_rate_of_return("BIL")    # SPDR Bloomberg Barclay 1-3 Month T-Bill : Cash
        if bil_ror is None:
            print("Warning: No data for BIL. Stopped.")
            return []

        if spy_ror > bil_ror:
            if spy_ror >= efa_ror:
                return ["SPY"]
            else:
                return ["IEFA"]
        else:
            return self._daa.calculate()

    def _calculate_rate_of_return(self, ticker):
        return self._common.calculate_rate_of_return(ticker, 12)
