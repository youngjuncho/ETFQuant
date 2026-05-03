# Adaptive Dual Momentum Strategy

class ADM:
    def __init__(self, common, daa):
        self._common = common
        self._daa = daa
        self._assets = [
            "SPY", # SPDR S&P 500 | US Stocks
            "EFA", # iShares MSCI EAFE : Developed Market Stocks
            "BIL", # SPDR Bloomberg Barclay 1-3 Month T-Bill : Cash
        ]

    async def calculate(self):
        rors = await self._common.calculate_rate_of_returns(self._assets, [12])
        
        try:
            spy_ror = rors["SPY"].get(12)
            efa_ror = rors["EFA"].get(12)
            bil_ror = rors["BIL"].get(12)
            
            if spy_ror is None or efa_ror is None or bil_ror is None:
                raise ValueError("Missing data")
        except (KeyError, ValueError):
            print("Warning: ADM 데이터 누락. DAA로 우회하거나 안전자산을 반환합니다.")
            return ["BIL"]

        if spy_ror > bil_ror:
            return ["SPY" if spy_ror >= efa_ror else "EFA"]
        else:
            return await self._daa.calculate()
