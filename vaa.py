# Vigilant Asset Allocation (VAA) - Aggressive Variant

class VAA:
    def __init__(self, common):
        self._common = common
        self._aggressive_assets = ["SPY", "VEA", "VWO", "BND"]
        self._safe_assets = ["SHY", "IEF", "LQD"]
        
        self._weights = [12, 4, 2, 1]
        self._periods = [1, 3, 6, 12]

    async def calculate(self):
        all_assets = list(set(self._aggressive_assets + self._safe_assets + ["BIL"]))
        
        rors = await self._common.calculate_rate_of_returns(all_assets, self._periods)
        prices = await self._common.get_prices(all_assets, [15])
        
        scores = {t: self._calculate_momentum_score(t, rors) for t in all_assets}

        is_aggressive = all(scores[t] > 0 for t in self._aggressive_assets)

        if is_aggressive:
            agg_dvs = self._calculate_divergences(self._aggressive_assets, prices)
            top_asset = max(agg_dvs, key=agg_dvs.get)
            return [top_asset]
        else:
            safe_scores = {t: scores[t] for t in self._safe_assets}
            top_safe = max(safe_scores, key=safe_scores.get)
            
            safe_dv = self._calculate_single_dv(top_safe, prices)
            return [top_safe] if (scores[top_safe] > 0 and safe_dv >= 1.0) else ["BIL"]

    def _calculate_momentum_score(self, ticker, rors):
        ticker_rors = rors.get(ticker, {})
        return sum(self._weights[i] * (ticker_rors.get(p) or 0) for i, p in enumerate(self._periods))

    def _calculate_divergences(self, tickers, prices):
        return {t: self._calculate_single_dv(t, prices) for t in tickers}

    def _calculate_single_dv(self, ticker, prices):
        df = prices.get(ticker)
        if df is None or df.empty or len(df) < 270: return 0
        return df['close'].iloc[-1] / df['close'].rolling(window=270).mean().iloc[-1]