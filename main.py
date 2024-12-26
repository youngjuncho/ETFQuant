from collections import Counter
from common import Common
from adm import ADM
from baa import BAA
from daa import DAA
from inverse import Inverse

common = Common()

daa = DAA(common)

adm = ADM(common, daa)
adm_portfolio = adm.calculate()
print(f"ADM : {adm_portfolio}")

baa = BAA(common)
baa_portfolio = baa.calculate()
print(f"BAA : {baa_portfolio}")

daa_portfolio = daa.calculate()
print(f"DAA : {daa_portfolio}")

inverse = Inverse(common)
inverse_portfolio_daa = inverse.calculate(6)
print(f"INV DAA : {inverse_portfolio_daa}")
inverse_portfolio_others = inverse.calculate(12)
print(f"INV Others : {inverse_portfolio_others}")

desired_len = 3
adm_portfolio.extend(adm_portfolio * (desired_len - len(adm_portfolio)))
baa_portfolio.extend(baa_portfolio * (desired_len - len(baa_portfolio)))
daa_portfolio.extend(daa_portfolio * (desired_len - len(daa_portfolio)))

portfolios = [adm_portfolio, baa_portfolio, daa_portfolio]
combined_portfolio = [item for sublist in portfolios for item in sublist]
counter = Counter(combined_portfolio)
portfolio = {item: "{:.1f}%".format(counter[item] / len(combined_portfolio) * 100) for item in counter}

print("")
for ticker, ratio in portfolio.items():
    print(f"\t{ticker} : {ratio}")
print("")