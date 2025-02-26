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
                raise ValueError(f"No data found for {ticker} in the given period")

            first_day_price = closing_price.iloc[0]
            last_day_price = closing_price.iloc[-1]

            return last_day_price / first_day_price - 1
        except Exception as e:
            print(f"Error calculating rate of return for {ticker_name}: {e}")
            return None
