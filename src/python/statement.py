import requests
from datetime import datetime as dt
from datetime import timedelta
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
from pycoingecko import CoinGeckoAPI
import dotenv
import os

CG = CoinGeckoAPI()
ETHER_VALUE = 1e18
BASE_URLs = {
    "eth":  "https://api.etherscan.io/api",
    "poly": "https://api.polygonscan.com/api",
    "arbi": "https://api.arbiscan.io/api"
}
CHAINS = dict(eth="ethereum",
              poly="matic-network",
              arbi="arbitrum")
API_KEYs = os.getenv("API_KEYs")
TODAY_DATE = dt.now().date()



def make_api_url(module, action, address, chain="eth", **kwargs):
    base_url = BASE_URLs[chain]
    api_key = API_KEYs[chain]
    url = base_url + f"?module={module}&action={action}&address={address}&apikey={api_key}"
    for k, v in kwargs.items():
        url += f"&{k}={v}"
    return url

def get_account_balance(address, chain="eth"):
    balance_url = make_api_url("account", "balance", address, chain=chain, tag="latest")
    response = requests.get(balance_url)
    data = response.json()

    return int(data["result"]) / ETHER_VALUE

def get_price(date, chain="eth", currency="usd"):
    res = CG.get_coin_history_by_id(id=CHAINS[chain], date=date.strftime("%d-%m-%Y"))
    return res["market_data"]["current_price"][currency]

def crypto_to_fiat(amt, crypto_chain="eth", fiat_type="usd", date=TODAY_DATE):
    rate = get_price(date, crypto_chain, fiat_type)
    return amt * rate

def get_transactions(address, chain="eth"):
    get_transactions_url = make_api_url("account", "txlist", address, chain=chain, startblock=0, endblock=999999999,
                                        page=1, offset=100, sort="desc")
    response = requests.get(get_transactions_url)
    data = response.json()["result"]

    get_in_transactions_url = make_api_url("account", "txlistinternal", address, chain=chain, startblock=0, endblock=999999999,
                                           page=1, offset=100, sort="dsc")
    response2 = requests.get(get_in_transactions_url)
    data.extend(response2.json()["result"])
    data.sort(key=lambda x: int(x["timeStamp"]), reverse=True)

    print(len(data))

    current_balance = get_account_balance(address)
    balances = [current_balance]
    times = []
    values = []
    status = []

    for i in range(len(data)):
        tx = data[i]

        # print(tx)

        to = tx["to"]
        from_ = tx["from"]
        value = int(tx["value"]) / ETHER_VALUE
        time = dt.fromtimestamp(int(tx["timeStamp"]))
        money_in = to.lower() == address.lower()
        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETHER_VALUE

        if money_in:
            current_balance -= value
            values.append(value)
        else:
            current_balance += value + gas
            values.append(- value - gas)

        if tx["contractAddress"] == "":
            status.append("external")
        else:
            status.append("internal")

        balances.append(current_balance)
        times.append(time)

    res = {"balances": balances[:-1], "times": times, "values": values, "status": status}
    return res

def get_balance_by_date(date, res):
    # earliest -> latest
    dates = res["times"]
    balances = res["balances"]
    N = len(dates)

    i = 0
    while i != N and dates[i].date() > date:
        i += 1

    if i == N:
        print("Need earlier records")
        return 0
    elif i == 0:
        print("Need more recent records")
        pass
        # return balances[0]

    return balances[i]

calendar = {"January": datetime.date(2023, 1, 31),
       "Feburary": datetime.date(2023, 2, 28),
        "March": datetime.date(2023, 3, 31),
        "April": datetime.date(2023, 4, 30),
        "May": datetime.date(2023, 5, 31),
        "June": datetime.date(2023, 6, 30),
       "July": datetime.date(2022, 7, 31),
       "August": datetime.date(2022, 8, 31),
       "September": datetime.date(2022, 9, 30),
       "October": datetime.date(2022, 10, 31),
       "November": datetime.date(2022, 11, 30),
       "December": datetime.date(2022, 12, 31)}

bs = []
for k,v in calendar.items():
    b = get_balance_by_date(v, res)
    print(f"{k} balance: {b}\n")
    bs.append(b)

# for k,v in res.items():
#     print(v)
sample_account = {
    "ETH": {
        "Wallet Address": ["0x6bd97627d084a7d4c476715031e00d99d9275d80",
                           "0x5C198D5C727C6D51Da451B44f9e759a79f84f743"],
    }
}

sample_account["ETH"]["Balance (ETH)"] = [get_account_balance(i) for i in sample_account["ETH"]["Wallet Address"]]
sample_account["ETH"]["Balance (USD equivalent)"] = [crypto_to_fiat(i) for i in sample_account["ETH"]["Balance (ETH)"]]

df_eth_account = pd.DataFrame(sample_account["ETH"])
df_eth_account["Balance (ETH)"] = np.round(df_eth_account["Balance (ETH)"], 2)
df_eth_account["Balance (USD equivalent)"] = np.round(df_eth_account["Balance (USD equivalent)"], 2)


##############################################################
import plotly.express as px
import plotly.graph_objects as go

# get pie chart
address = "0x5C198D5C727C6D51Da451B44f9e759a79f84f743"
curr_account = {}
for chain,v in CHAINS.items():
    curr_account[chain] = crypto_to_fiat(get_account_balance(address, chain), chain)
    print(curr_account[chain])


# get bar plot




# header = dict(
#     values=["Date", "Description, ""Balance"],
#     fill_color=headerColor,
#     align=['left', 'center'],
#     font=dict(color='white', size=12)
# )
#
# cells = dict(
#     values=[res["times"], res["status"], res["balances"]],
#     line_color='darkslategray',
#     # 2-D list of colors for alternating rows
#     fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
#     align = ['left', 'center'],
#     font = dict(color = 'darkslategray', size = 11)
#     )
#
# fig = go.Figure(data=[go.Table(
#   header=header,
#   cells=cells)
# ])
#
# fig.update_layout(
#     autosize=False,
#     width=500,
#     height=500)
#
# fig.write_image("/Users/guoziting/Desktop/capychain/test.png")