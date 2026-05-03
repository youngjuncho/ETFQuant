# Hybrid Asset Allocation Strategy

class HAA:
    def __init__(self, common):
        self._common = common
        self._aggressive_assets = [
            "SPY", # 미국 대형주
            "IWM", # 미국 소형주
            "VEA", # 선진국 주식
            "VWO", # 신흥국 주식
            "VNQ", # 미국 리츠
            "DBC"  # 원자재
        ]
        self._safe_assets = ["IEF", "BIL"] 
        self._canary_asset = "TIP"
        
        self._weights = [12, 4, 2, 1]
        self._periods = [1, 3, 6, 12]

    async def calculate(self):
        canary_rors = await self._common.calculate_rate_of_returns([self._canary_asset], self._periods)
        canary_score = self._calculate_momentum_score(self._canary_asset, canary_rors)

        all_assets = list(set(self._aggressive_assets + self._safe_assets))
        prices = await self._common.get_prices(all_assets, [15])

        if canary_score > 0:
            agg_dvs = self._calculate_divergences(self._aggressive_assets, prices)
            if not agg_dvs: return ["BIL"]
            
            top_asset = max(agg_dvs, key=agg_dvs.get)
            return [top_asset]
        else:
            safe_dvs = self._calculate_divergences(self._safe_assets, prices)
            top_safe = max(safe_dvs, key=safe_dvs.get)
            return [top_safe]

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