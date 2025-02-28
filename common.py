import warnings
import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta
from yahooquery import Ticker

warnings.simplefilter(action='ignore', category=FutureWarning)

class Common:
    def __init__(self):
        pass

    def get_prices(self, tickers, periods):
        prices = self._fetch_prices(tickers, periods)
        if prices.empty:
            print("Warning: No price data available")
            return {ticker: pd.DataFrame() for ticker in tickers}

        return {ticker: prices[prices['symbol'] == ticker].reset_index(drop=True) for ticker in tickers}

    def calculate_rate_of_returns(self, tickers, periods):
        prices = self._fetch_prices(tickers, periods)
        if prices.empty:
            print("Warning: No price data available")
            return {ticker: {period: None for period in periods} for ticker in tickers}

        return self._calculate_rate_of_return(prices, tickers, periods)

    def _fetch_prices(self, tickers, periods):
        end_date = datetime.today().replace(tzinfo=None)
        begin_date = end_date - relativedelta(months=max(periods))

        try:
            prices = Ticker(tickers).history(start=begin_date, end=end_date)['close'].reset_index(level=0, drop=False)
            if prices.empty:
                print(f"Warning: No price data available for {tickers}")
                return pd.DataFrame()

            if isinstance(prices.index, pd.DatetimeIndex):
                prices.index = prices.index.tz_localize(None)

            return prices

        except Exception as e:
            print(f"Error get prices for tickers: {e}")
            return pd.DataFrame()

    def _calculate_rate_of_return(self, prices, tickers, periods):
        results = {ticker: {} for ticker in tickers}
        end_date = datetime.today().replace(tzinfo=None)

        for ticker in tickers:
            price = prices[prices['symbol'] == ticker].reset_index()
            if 'date' not in price.columns:
                print(f"Error: 'date' column not found in price data for {ticker}")
                for period in periods:
                    results[ticker][period] = None
                continue

            price['date'] = pd.to_datetime(price['date'], utc=True)
            price['date'] = price['date'].dt.tz_localize(None)

            if price.empty:
                print(f"Warning: No price for {ticker}. Skipping...")
                for period in periods:
                    results[ticker][period] = None
                continue

            begin_dates = {period: end_date - relativedelta(months=period) for period in periods}
            for period, begin_date in begin_dates.items():
                try:
                    closest_idx = (price['date'] - begin_date).abs().idxmin()
                    first_day_price = price.loc[closest_idx, 'close']
                    last_day_price = price.iloc[-1]['close']
                    results[ticker][period] = last_day_price / first_day_price - 1
                except Exception as e:
                    print(f"Error in calculating rate of return for {ticker}, period {period}: {e}")
                    results[ticker][period] = None

        return results
