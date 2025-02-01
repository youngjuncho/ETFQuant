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

    def calculate(self):
        # aggressive_asset_rors = {ticker: self._calculate_rate_of_return(ticker) for ticker in self._aggressive_assets}
        aggressive_asset_rors = {ticker: ror for ticker, ror in
                                 ((ticker, self._calculate_rate_of_return(ticker)) for ticker in
                                  self._aggressive_assets) if ror is not None}
        top3_aggressive_assets = [ticker for ticker, v in
                                  sorted(aggressive_asset_rors.items(), key=lambda x: x[1], reverse=True)[:3]]

        if any(ror < 0 for ticker, ror in aggressive_asset_rors.items() if ticker in top3_aggressive_assets):
            return self._safe_assets
        else:
            return top3_aggressive_assets

    def _calculate_rate_of_return(self, ticker):
        ror = self._common.calculate_rate_of_return(ticker, 6)
        if ror is None:
            print(f"Warning: Rate of return for {ticker} could not be calculated.")
        return ror
