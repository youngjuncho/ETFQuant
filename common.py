import yfinance as yf

from datetime import datetime
from dateutil.relativedelta import relativedelta

class Common:
    def __init__(self):
        pass

    def calculate_rate_of_return(self, ticker, period):
        end_date = datetime.today()
        begin_date = end_date - relativedelta(months=period)

        closing_price = yf.download(ticker, start=begin_date, end=end_date, progress=False)['Close']

        first_day_price = closing_price.iloc[0]
        last_day_price = closing_price.iloc[-1]

        return last_day_price / first_day_price - 1
