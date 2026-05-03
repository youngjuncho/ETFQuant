# Bold Asset Allocation Strategy

class BAA:
    def __init__(self, common):
        self._common = common
        self._aggressive_assets = [
            "QQQ", # Invesco QQQ Trust | NASDAQ
            "EFA", # iShares Core MSCI EAFE : Developed Market Stocks
            "EEM", # iShares MSCI Emerging Markets : Emerging Market Stocks
            "GLD", # SPDR Gold Shares
            "DBC"  # Invesco DB Commodity Index Tracking Fund
        ]
        self._safe_assets = [
            "TLT", # iShares 20+ Year Treasury Bond : US Long-term Bond
            "TIP", # iShares TIPS Bond : US Inflation-linked Bond
            "DBC", # Invesco DB Commodity Index Tracking Fund
            "AGG", # iShares Core US Aggregate Bond : US Mixed Bonds
            "LQD", # iShares iBoxx $ Investment Grade Corporate Bond : US Corporate Bonds
            "IEF", # iShares 7-10 Year Treasury Bond : US Intermediate-Term Bonds
            "BIL"  # SPDR Bloomberg Barclays 1-3 Month T-Bill : Cash
        ]
        self._canary_assets = [
            "SPY", # SPDR S&P 500 | US Stocks
            "EFA", # iShares Core MSCI EAFE : Developed Market Stocks
            "EEM", # iShares MSCI Emerging Markets : Emerging Market Stocks
            "AGG"  # iShares Core US Aggregate Bond : US Mixed Bonds
        ]
        self._weights = [12, 4, 2, 1]
        self._periods = [1, 3, 6, 12]

    async def calculate(self):
        all_assets = list(set(self._aggressive_assets + self._safe_assets + self._canary_assets))

        rors = await self._common.calculate_rate_of_returns(self._canary_assets, self._periods)
        prices = await self._common.get_prices(all_assets, [15]) # 13 -> 15 수정

        canary_asset_mss = {ticker: self._calculate_momentum_score(ticker, rors) for ticker in self._canary_assets}

        aggressive_asset_dvs = self._calculate_divergences(self._aggressive_assets, prices)
        safe_asset_dvs = self._calculate_divergences(self._safe_assets, prices)

        if any(ms < 0 for ms in canary_asset_mss.values()):
            top3_safe_assets = sorted(safe_asset_dvs, key=safe_asset_dvs.get, reverse=True)[:3]
            bil_dv = safe_asset_dvs.get("BIL", 0)
            return [ticker if safe_asset_dvs.get(ticker, 0) >= bil_dv else "BIL" for ticker in top3_safe_assets]
        else:
            top_aggressive_asset = max(aggressive_asset_dvs, key=aggressive_asset_dvs.get, default=None)
            return [top_aggressive_asset] if top_aggressive_asset else []

    def _calculate_momentum_score(self, ticker, rors):
        ticker_rors = rors.get(ticker, {})
        return sum(self._weights[i] * (ticker_rors.get(period) or 0) for i, period in enumerate(self._periods))

    def _calculate_divergences(self, tickers, prices):
        divergences = {}
        for ticker in tickers:
            df = prices.get(ticker)
            if df is None or df.empty or len(df) < 270:
                divergences[ticker] = 0
                continue
            latest_price = df['close'].iloc[-1]
            moving_average = df['close'].rolling(window=270).mean().iloc[-1]
            divergences[ticker] = latest_price / moving_average if moving_average else 0
        return divergences
