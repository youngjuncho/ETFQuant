# Bold Asset Allocation Strategy

import yfinance as yf

from datetime import datetime
from dateutil.relativedelta import relativedelta

class BAA:
    def __init__(self, common):
        self._common = common
        self._aggressive_assets = [
            "QQQ",  # Invesco QQQ Trust | NASDAQ
            "IEFA", # iShares Core MSCI EAFE : Developed Market Stocks
            "IEMG", # iShares Core MSCI Emerging Markets : Emerging Market Stocks
            "AGG"   # iShares Core US Aggregate Bond : US Mixed Bonds
        ]
        self._safe_assets = [
            "TLT",  # iShares 20+ Year Treasury Bond : US Long-term Bond
            "TIP",  # iShares TIPS Bond : US Inflation-linked Bond
            "PDBC", # Invesco Optimum Yield Diversified Commodity Strategy No K-1 : Commodities
            "AGG",  # iShares Core US Aggregate Bond : US Mixed Bonds
            "LQD",  # iShares iBoxx $ Investment Grade Corporate Bond : US Corporate Bonds
            "IEF",  # iShares 7-10 Year Treasury Bond : US Intermediate-Term Bonds
            "BIL"   # SPDR Bloomberg Barclays 1-3 Month T-Bill : Cash
        ]
        self._canary_assets = [
            "SPY",  # SPDR S&P 500 | US Stocks
            "IEFA", # iShares Core MSCI EAFE : Developed Market Stocks
            "IEMG", # iShares Core MSCI Emerging Markets : Emerging Market Stocks
            "AGG"   # iShares Core US Aggregate Bond : US Mixed Bonds
        ]
        self._weights = [12, 4, 2, 1]
        self._periods = [1, 3, 6, 12]

    def calculate(self):
        canary_asset_mss = [self._calculate_momentum_score(ticker) for ticker in self._canary_assets]
        try:
            aggressive_asset_dvs = {ticker: self._calculate_divergence(ticker) for ticker in self._aggressive_assets}
        except Exception as e:
            print(f"Error calculating divergence for aggressive assets: {e}")
            aggressive_asset_dvs = {}
        top_aggressive_asset = [ticker for ticker, v in
                                sorted(aggressive_asset_dvs.items(), key=lambda x: x[1], reverse=True)[:1]]
        try:
            safe_asset_dvs = {ticker: self._calculate_divergence(ticker) for ticker in self._safe_assets}
        except Exception as e:
            print(f"Error calculating divergence for safe assets: {e}")
            safe_asset_dvs = {}
        top3_safe_assets = [ticker for ticker, v in
                            sorted(safe_asset_dvs.items(), key=lambda x: x[1], reverse=True)[:3]]

        if any(ms < 0 for ms in canary_asset_mss):
            return [ticker if safe_asset_dvs[ticker] > safe_asset_dvs["BIL"] else "BIL" for ticker in top3_safe_assets]
        else:
            return top_aggressive_asset

    def _calculate_momentum_score(self, ticker):
        total_score = 0
        for weight, period in zip(self._weights, self._periods):
            ror = self._calculate_rate_of_return(ticker, period)
            total_score += weight * (ror if ror is not None else 0)
        return total_score

    def _calculate_rate_of_return(self, ticker, period):
        try:
            return self._common.calculate_rate_of_return(ticker, period)
        except Exception as e:
            print(f"Error calculating rate of return for {ticker}: {e}")
            return None

    def _calculate_divergence(self, ticker):
        try:
            end_date = datetime.today()
            begin_date = end_date - relativedelta(months=13)

            data = yf.download(ticker, start=begin_date, end=end_date, progress=False)
            if data.empty:
                print(f"No data found for {ticker}.")
                return 0

            latest_price = data['Close'].iloc[-1]

            data['moving_average'] = data['Close'].rolling(window=270).mean()
            moving_average = data['moving_average'].iloc[-1]
            if moving_average == 0:
                print("Warning: moving_average is 0")
                return 0

            return latest_price / moving_average
        except Exception as e:
            print(f"Error calculating divergence for {ticker}: {e}")
            return 0
