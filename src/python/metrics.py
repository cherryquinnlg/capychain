import os

import numpy as np
import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime
from datetime import datetime as dt
import scipy

CG = CoinGeckoAPI()
TODAY_DATE = dt.now().date()
CHAINS = dict(eth="ethereum",
              poly="polygon",
              arbi="arbitrum")

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
RISK_FREE_RATE = os.getenv("risk_free_rate")
INDIVIDUAL_SHARPE_RATIOS = os.getenv("crypto_sharpe_ratios")
def get_portfolio_sharpe_ratio(weights):
    # Calculate portfolio return and standard deviation
    portfolio_return = np.dot(weights, INDIVIDUAL_SHARPE_RATIOS)
    portfolio_std_dev = np.sqrt(np.dot(weights ** 2, INDIVIDUAL_SHARPE_RATIOS ** 2))

    # Calculate excess return (portfolio return - risk-free rate)
    excess_return = portfolio_return - RISK_FREE_RATE

    # Calculate Sharpe ratio
    sharpe_ratio = excess_return / portfolio_std_dev

    return sharpe_ratio

def get_maximum_drawdown(returns):
    cumulative_returns = np.cumprod(1 + returns)  # Calculate cumulative returns
    peak = np.maximum.accumulate(cumulative_returns)  # Find the peak value
    drawdown = (cumulative_returns - peak) / peak  # Calculate drawdown
    max_drawdown = np.max(drawdown)  # Find the maximum drawdown

    return max_drawdown

def calculate_yearly_var(returns, level=0.95):
    mean_return = np.mean(returns)  # Calculate the mean return
    std_dev = np.std(returns)  # Calculate the standard deviation
    z_score = scipy.stats.norm.ppf(1-level)  # Calculate the z-score for the 95% confidence level
    yearly_std_dev = std_dev * np.sqrt(252)  # Convert the standard deviation to a yearly basis
    yearly_var = mean_return - (z_score * yearly_std_dev)  # Calculate the yearly VaR

    return yearly_var
