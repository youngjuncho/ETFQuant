# Dynamic Asset Allocation with Bonds Strategy

class DAA:
    def __init__(self, common):
        self._common = common
        self._aggressive_assets = [
            "SHY",  # iShares 1-3 Year Treasury Bond : US Short-term Government Bonds
            "TIP",  # iShares TIPS Bond : US Treasury Inflation-Protected Securities
            "IEF",  # iShares 7-10 Year Treasury Bond : US Intermediate-Term Bonds
            "LQD",  # iShares iBoxx $ Investment Grade Corporate Bond : US Corporate Bonds
            "TLT",  # iShares 20+ Year Treasury Bond : US Long-term Treasury Bonds
            "HYG",  # iShares iBoxx $ High Yield Corporate Bond : US High-Yield Bonds
            "BWX",  # SPDR Bloomberg Barclays International Treasury Bond : Developed Market Bonds
            "EMB"   # iShares JP Morgan USD Emerging Markets Bond | Emerging Market Bonds
        ]
        self._safe_assets = [
            "BIL"  # SPDR Bloomberg Barclays 1-3 Month T-Bill : Cash
        ]

    async def calculate(self):
        rors = await self._common.calculate_rate_of_returns(self._aggressive_assets, [6])
        valid_rors = {ticker: ror.get(6, None) for ticker, ror in rors.items() if ror.get(6, None) is not None}
        if not valid_rors:
            print("Warning: No valid aggressive asset rors. Defaulting to safe assets.")
            return self._safe_assets

        top3_aggressive_assets = sorted(valid_rors, key=valid_rors.get, reverse=True)[:3]
        if any(valid_rors[ticker] < 0 for ticker in top3_aggressive_assets):
            return self._safe_assets
        return top3_aggressive_assets
