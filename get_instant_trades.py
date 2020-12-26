import requests
import json
from datetime import datetime
import w3_test
from pycoingecko import CoinGeckoAPI
#from bs4 import BeautifulSoup

cg = CoinGeckoAPI()

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def get_trades():
    '''web_req = requests.get('https://etherscan.io/token/0xa4eed63db85311e22df4473f87ccfc3dadcfa3e3')
    content = BeautifulSoup(web_req.text, 'html.parser')
    assets = content.select('tbody  tr')
    print('akka')'''

    response = requests.get('https://api.etherscan.io/api?module=account&action=txlistinternal&address=0x7367409E0c12b2B7cAa5c990E11A75E0D86580fc&startblock=0&endblock=1149709300&page=1&offset=10&sort=desc&apikey=QCY854HHJW8I47RIIJRUH9WYASWI9VB1D1')
    json_data = json.loads(response.text)
    last_timestamp = json_data['result'][0]['timeStamp']
    #dt_object = datetime.fromtimestamp(int(last_timestamp))

    curr_obj = w3_test.get_currency(json_data['result'][0]['hash'])

    currency_address = curr_obj[0]
    curr = cg.get_coin_info_from_contract_address_by_id(id='ethereum', contract_address=currency_address)
    #curr_name = curr['name']
    value = curr_obj[2]
    curr_symb = curr['symbol'].upper()

    usdt_price = 1/cg.get_price(ids='tether', vs_currencies='usd')['tether']['usd']
    usd_price = curr['market_data']['current_price']['usd']
    usdt_itog = toFixed(curr_obj[1]*usd_price*usdt_price, 5)

    string_transaction = 'New SWAP transaction!\n' + \
                         str(value) + ' ETH to ' + str(curr_obj[1]) + ' ' + curr_symb + ' ('\
                         + str(usdt_itog)+' USDT)\n' \
                         'Transaction Hash: ' + json_data['result'][0]['hash']

    return last_timestamp, string_transaction

hey = get_trades()
print(hey[1])

def get_erc_trades():
    response = requests.get('https://api.etherscan.io/api?module=account&action=tokentx&address=0x7367409E0c12b2B7cAa5c990E11A75E0D86580fc&startblock=0&endblock=999999999&sort=desc&apikey=QCY854HHJW8I47RIIJRUH9WYASWI9VB1D1')
    json_data = json.loads(response.text)
    last_timestamp = json_data['result'][0]['timeStamp']

    return last_timestamp

#hey2 = get_erc_trades()

def healthcheck():
    response = requests.get('https://api.1inch.exchange/v2.0/healthcheck')
    json_data = json.loads(response.text)
    return json_data['status']

#healthcheck()

def get_course():
    response = requests.get('https://api.1inch.exchange/v2.0/quote?fromTokenAddress=0xa4eed63db85311e22df4473f87ccfc3dadcfa3e3&toTokenAddress=0x0000000000000000000000000000000000000000&amount=1000000000000000000')
    json_data = json.loads(response.text)
    one_inch_course = float(int(json_data['toTokenAmount'])/1000000000000000000)
    #coingecko_course = requests.get('https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=0xa4eed63db85311e22df4473f87ccfc3dadcfa3e3&vs_currencies=eth')
    coingecko_course = float(cg.get_price(ids='rubic', vs_currencies='eth')['rubic']['eth'])

    ### count difference between 1inch and coingecko
    coingecko_percent = 100/one_inch_course*coingecko_course
    diff = abs(100.0 - coingecko_percent)
    return diff

#print(get_course())
