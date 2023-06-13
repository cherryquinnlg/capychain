import numpy as np
import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime

CG = CoinGeckoAPI()

CHAINS = dict(eth="ethereum",
              poly="polygon",
              arbi="arbitrum")

TODAY_DATE = datetime.date(2023, 5, 31)
TODAY_DATE.strftime("%s")

today_date = datetime.date(2023, 5, 31)
may_date = datetime.date(2020, 5, 31)
apr_date = datetime.date(2020, 4, 30)

#################################################################################
def get_price(date, chain="eth", currency="usd"):
    res = CG.get_coin_history_by_id(id=CHAINS[chain], date=date.strftime("%d-%m-%Y"))
    return res["market_data"]["current_price"][currency]

def get_price_series(chain="eth", currency="usd", from_date=TODAY_DATE, to_date=TODAY_DATE):
    res = CG.get_coin_market_chart_range_by_id(id=CHAINS[chain], vs_currency=currency,
                                     from_timestamp=from_date.strftime("%s"), to_timestamp=to_date.strftime("%s"))
    dates = [datetime.fromtimestamp(p[0] // 1000).date() for p in res["prices"]]
    prices = [p[1] for p in res["prices"]]

    return {"dates": dates, "prices": prices}

price_series = get_price_series()
def get_portfolio_sharpe_ratio():

def get_portfolio_value_at_risk():
