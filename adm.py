# Adaptive Dual Momentum Strategy

import yfinance as yf

from datetime import datetime
from dateutil.relativedelta import relativedelta
from daa import DAA

class ADM:
    def __init__(self):
        pass

    def calculate(self):
        spy_ror = self._calculate_rate_of_return("SPY")    # SPDR S&P 500 | US Stocks
        efa_ror = self._calculate_rate_of_return("EFA")    # iShares MSCI EAFE : Developed Market Stocks
        bil_ror = self._calculate_rate_of_return("BIL")    # SPDR Bloomberg Barclay 1-3 Month T-Bill : Cash

        if spy_ror > bil_ror:
            if spy_ror >= efa_ror:
                return ["SPY"]
            else:
                return ["EFA"]
        else:
            return DAA().calculate()

    def _calculate_rate_of_return(self, ticker, period=12):
        end_date = datetime.today()
        begin_date = end_date - relativedelta(months=period)

        closing_price = yf.download(ticker, start=begin_date, end=end_date, progress=False)['Close']

        first_day_price = closing_price.iloc[0]
        last_day_price = closing_price.iloc[-1]

        return last_day_price / first_day_price - 1
