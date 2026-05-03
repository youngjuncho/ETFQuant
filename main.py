import asyncio
from datetime import datetime
from common import Common
from adm import ADM
from baa import BAA
from daa import DAA
from haa import HAA
from vaa import VAA

async def main():
    try:
        common = Common()
        daa = DAA(common)
        
        strategy_map = {
            "ADM" : ADM(common, daa),
            "BAA" : BAA(common),
            "DAA" : daa,
            "HAA" : HAA(common),
            "VAA" : VAA(common)
        }

        names, results = await run_strategies(strategy_map)
        show_individual_results(names, results)
        final_portfolio = combine_portfolios(results)
        show_final_portfolio(final_portfolio)

    except Exception as e:
        print(f"\n[Error occurred]: {e}")

async def run_strategies(strategy_map):
    names = list(strategy_map.keys())
    tasks = [s.calculate() for s in strategy_map.values()]
    results = await asyncio.gather(*tasks)
    return names, results

def show_individual_results(names, results):
    for name, res in zip(names, results):
        res_display = ", ".join(res) if res else "BIL"
        print(f"{name} : [ {res_display} ]")

def combine_portfolios(results_list):
    mapping_table = {
        "SPY": "SPYM", "QQQ": "QQQM", "IWM": "VTWO", "EFA": "VEA",
        "EEM": "IEMG", "VWO": "IEMG", "AGG": "BND", "BIL": "SGOV",
        "SHY": "SCHO", "IEF": "VGIT", "TLT": "VGLT", "TIP": "SCHP",
        "LQD": "VCIT", "HYG": "SPHY", "BWX": "BNDX", "EMB": "VWOB",
        "GLD": "GLDM", "DBC": "PDBC", "VNQ": "USRT", "SLV": "SIVR"
    }
    combined = {}

    total_strategies = len(results_list)

    for res in results_list:
        if not res: continue
        weight_per_asset = (1.0 / total_strategies) / len(res)
        for ticker in res:
            final_ticker = mapping_table.get(ticker, ticker)
            combined[final_ticker] = combined.get(final_ticker, 0) + weight_per_asset

    return {t: round(w, 4) for t, w in combined.items()}

def show_final_portfolio(final_portfolio):
    sorted_portfolio = sorted(final_portfolio.items(), key=lambda x: x[1], reverse=True)
    for ticker, weight in sorted_portfolio:
        if weight > 0:
            print(f"[{ticker:^6}] : {weight*100:>5.2f}%")

if __name__ == "__main__":
    asyncio.run(main())