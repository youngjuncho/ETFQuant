# Inverse ETFs

class Inverse:
    def __init__(self, common):
        self._common = common
        self._assets = [
            "SH",  # ProShares Short S&P500
            "PSQ",  # ProShares Short QQQ
            "BIL"  # SPDR Bloomberg Barclay 1-3 Month T-Bill : Cash
        ]

    async def calculate(self, periods):
        rors = await self._common.calculate_rate_of_returns(self._assets, periods)
        best_assets = {}
        for period in periods:
            period_rors = {ticker: rors.get(ticker, {}).get(period, None) for ticker in self._assets}
            period_rors = {ticker: ror for ticker, ror in period_rors.items() if ror is not None}
            best_assets[period] = [ticker for ticker, _ in
                                   sorted(period_rors.items(), key=lambda x: x[1], reverse=True)]

        return best_assets
