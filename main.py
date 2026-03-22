from asyncio import gather, run
from collections import Counter
from common import Common
from adm import ADM
from baa import BAA
from daa import DAA

async def main():
    common = Common()
    daa = DAA(common)
    adm = ADM(common, daa)
    baa = BAA(common)

    adm_portfolio, baa_portfolio, daa_portfolio = await gather(
        adm.calculate(),
        baa.calculate(),
        daa.calculate(),
    )

    print(f"ADM : {adm_portfolio}")
    print(f"BAA : {baa_portfolio}")
    print(f"DAA : {daa_portfolio}")

    adm_portfolio = get_extended_portfolio(adm_portfolio)
    baa_portfolio = get_extended_portfolio(baa_portfolio)
    daa_portfolio = get_extended_portfolio(daa_portfolio)

    combined_portfolio = adm_portfolio + baa_portfolio + daa_portfolio
    counter = Counter(combined_portfolio)
    portfolio = {item: f"{(count / len(combined_portfolio) * 100):.1f}%" for item, count in counter.items()}

    show_portfolio(portfolio)

def get_extended_portfolio(portfolio, desired_length=3):
    return portfolio * (desired_length // len(portfolio)) + portfolio[:desired_length % len(portfolio)]

def show_portfolio(portfolio):
    print("")
    for ticker, ratio in portfolio.items():
        print(f"\t{ticker} : {ratio}")
    print("")

run(main())
