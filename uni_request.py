import requests
import json
from datetime import datetime
import w3_test
from pycoingecko import CoinGeckoAPI
import os
from uniswap import Uniswap

def uni_req():
    response = requests.get('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2?')
    json_data = json.loads(response.text)