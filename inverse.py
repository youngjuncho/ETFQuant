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
        rors = {}

        for ticker in self._assets:
            ror = self._common.calculate_rate_of_return(ticker, period)
            if ror is None:
                print(f"Warning: No data or error for {ticker}. Skipping...")
            else:
                rors[ticker] = ror

        return [ticker for ticker, v in sorted(rors.items(), key=lambda x: x[1], reverse=True)]
