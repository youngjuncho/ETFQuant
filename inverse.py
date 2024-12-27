# Inverse ETFs

class Inverse:
    def __init__(self, common):
        self._common = common
        self._assets = [
            "SH",   # ProShares Short S&P500
            "PSQ",  # ProShares Short QQQ
            "BIL"   # SPDR Bloomberg Barclay 1-3 Month T-Bill : Cash
        ]

    def calculate(self, period):
        rors = {ticker: self._common.calculate_rate_of_return(ticker, period) for ticker in self._assets}
        return [ticker for ticker, v in sorted(rors.items(), key=lambda x: x[1], reverse=True)]
