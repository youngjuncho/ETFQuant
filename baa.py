# Bold Asset Allocation Strategy

import yfinance as yf

from datetime import datetime
from dateutil.relativedelta import relativedelta

class BAA:
    def __init__(self):
        self._aggressive_assets = [
            "QQQ",  # Invesco QQQ Trust | NASDAQ
            "EFA",  # iShares MSCI EAFE : Developed Market Stocks
            "EEM",  # iShares MSCI Emerging Markets : Emerging Market Stocks
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
            "EFA",  # iShares MSCI EAFE : Developed Market Stocks
            "EEM",  # iShares MSCI Emerging Markets : Emerging Market Stocks
            "AGG"   # iShares Core US Aggregate Bond : US Mixed Bonds
        ]

    def calculate(self):
        canary_asset_mss = [self._calculate_momentum_score(ticker) for ticker in self._canary_assets]
        aggressive_asset_dvs = {ticker: self._calculate_divergence(ticker) for ticker in self._aggressive_assets}
        top_aggressive_asset = [ticker for ticker, v in sorted(aggressive_asset_dvs.items(), key=lambda x: x[1], reverse=True)[:1]]
        safe_asset_dvs = {ticker: self._calculate_divergence(ticker) for ticker in self._safe_assets}
        top_3_safe_assets = [ticker for ticker, v in sorted(safe_asset_dvs.items(), key=lambda x: x[1], reverse=True)[:3]]

        if any(ms < 0 for ms in canary_asset_mss):
            return [ticker if safe_asset_dvs[ticker] > safe_asset_dvs["BIL"] else "BIL" for ticker in top_3_safe_assets]
        else:
            return top_aggressive_asset

    def _calculate_momentum_score(self, ticker):
        return 12 * self._calculate_rate_of_return(ticker, 1) + 4 * self._calculate_rate_of_return(ticker, 3) \
            + 2 * self._calculate_rate_of_return(ticker, 6) + 1 * self._calculate_rate_of_return(ticker, 12)

    def _calculate_rate_of_return(self, ticker, period):
        end_date = datetime.today()
        begin_date = end_date - relativedelta(months=period)

        closing_price = yf.download(ticker, start=begin_date, end=end_date, progress=False)['Close']
        first_day_price = closing_price.iloc[0]
        last_day_price = closing_price.iloc[-1]

        return last_day_price / first_day_price - 1

    def _calculate_divergence(self, ticker):
        end_date = datetime.today()
        begin_date = end_date - relativedelta(months=13)

        data = yf.download(ticker, start=begin_date, end=end_date, progress=False)

        latest_price = data['Close'].iloc[-1]

        data['moving_average'] = data['Close'].rolling(window=270).mean()
        moving_average = data['moving_average'].iloc[-1]

        return latest_price / moving_average
