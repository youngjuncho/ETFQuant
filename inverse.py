# Inverse ETFs

class Inverse:
    def __init__(self, common):
        self._common = common
        self._assets = [
            "SH",  # ProShares Short S&P500
            "PSQ",  # ProShares Short QQQ
            "BIL"  # SPDR Bloomberg Barclay 1-3 Month T-Bill : Cash
        ]

    def calculate(self, period):
        rors = self._common.calculate_rate_of_returns(self._assets, period)
        valid_rors = {ticker: ror for ticker, ror in rors.items() if ror is not None}

        return [ticker for ticker, v in sorted(valid_rors.items(), key=lambda x: x[1], reverse=True)]
