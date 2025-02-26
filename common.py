import warnings

from datetime import datetime
from dateutil.relativedelta import relativedelta
from yahooquery import Ticker

warnings.simplefilter(action='ignore', category=FutureWarning)

class Common:
    def __init__(self):
        pass

    def calculate_rate_of_return(self, ticker_name, period):
        try:
            end_date = datetime.today()
            begin_date = end_date - relativedelta(months=period)

            ticker = Ticker(ticker_name)
            closing_price = ticker.history(start=begin_date, end=end_date)['close'].reset_index(level=0, drop=True)
            if closing_price.empty:
                raise ValueError(f"No data found for {ticker_name} in the given period")

            first_day_price = closing_price.iloc[0]
            last_day_price = closing_price.iloc[-1]

            return last_day_price / first_day_price - 1
        except Exception as e:
            print(f"Error calculating rate of return for {ticker_name}: {e}")
            return None

    def calculate_rate_of_returns(self, ticker_names, period):
        end_date = datetime.today()
        begin_date = end_date - relativedelta(months=period)
        tickers = Ticker(ticker_names)
        prices = self._get_prices(tickers, begin_date, end_date)
        if prices.empty:
            return {ticker_name: None for ticker_name in ticker_names}

        return self._calculate_rate_of_return(prices, ticker_names)

    def _get_prices(self, tickers, begin_date, end_date):
        try:
            return tickers.history(start=begin_date, end=end_date)['close'].reset_index(level=0, drop=False)
        except Exception as e:
            print(f"Error get prices for tickers: {e}")
            return pd.DataFrame()

    def _calculate_rate_of_return(self, prices, ticker_names):
        results = {}

        for ticker_name in ticker_names:
            price = prices[prices['symbol'] == ticker_name]
            if price.empty:
                print(f"Warning: No price for {ticker_name}. Skipping...")
                results[ticker_name] = None
                continue

            first_day_price = price.iloc[0]['close']
            last_day_price = price.iloc[-1]['close']
            results[ticker_name] = last_day_price / first_day_price - 1

        return results
