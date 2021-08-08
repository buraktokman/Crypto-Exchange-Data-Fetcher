#!/usr/bin/env python3
'''
Cryptowat.ch API
https://cryptowat.ch/docs/api
https://api.cryptowat.ch/markets/gdax/btcusd/summary '''

import urllib.request, json, datetime, time
from urllib.request import urlopen
from pathlib import Path

csv_file_price = Path(__file__).parents[0] / 'data' / 'price' / 'cryptowatch-bitcoin-price.csv'
csv_file_vol = Path(__file__).parents[0] / 'data' / 'volume' / 'cryptowatch-bitcoin-vol.csv'
exchanges = [
    'bitfinex',
    'gdax',
    'bitstamp',
    'kraken',
    'gemini',
    'cexio',
    'btce',
    'quoine',
    'okcoin',
    'bitsquare' ]

def request(url):
    '''limit = 1000
    since = 1481663244
    payload = {
        'limit':limit,
        'since':since }
    try:
        resp = requests.post(url, params=payload)
        return resp
    except Exception as e:
        print('couldnt fetch data from cryptowat.ch')'''

    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    print(data)

    return data['result']['price']['last'], data['result']['volume']

def main():
    price_s = ''
    volume_s = ''
    price_a = []
    volume_a = []

    current_time = datetime.datetime.now(datetime.timezone.utc)
    unix_timestamp = current_time.timestamp()
    print(int(unix_timestamp))

    for x in range(len(exchanges)):
        print(exchanges[x])
        url = 'https://api.cryptowat.ch/markets/' + exchanges[x] + '/btcusd/summary'
        try:
            price, volume = request(url)
        except Exception as e:
            price, volume = None,None

        # prices to string
        if x == 0:
            price_s = str(price) # format(price,'.3f')
        elif x < len(exchanges):
            price_s = price_s + ',' + str(price)

        # volumes to string
        if x == 0:
            volume_s = str(volume)
        elif x < len(exchanges):
            volume_s = volume_s + ',' + str(volume)

        price_a.append(price)
        volume_a.append(volume)
        print('price: ' + str(price))
        print('volume: ' + str(volume))

    with open(csv_file_price, 'a') as f:
        f.write(str(int(unix_timestamp)) + ',' + price_s + '\n')

    with open(csv_file_vol, 'a') as f:
        f.write(str(int(unix_timestamp)) + ',' + volume_s + '\n')

if __name__ == '__main__':
    #main()
    while True:
        now = datetime.datetime.now()
        while (now.second % 5):
            now = datetime.datetime.now()
            print(now.second)
            time.sleep(0.5)
        main()

    '''
    Exchanges that are do not trade BTC/USD
    quadrigacx
    bitMEX
    binance
    bithumb
    bittrex
    poloniex
    bitflyer
    bitvc
    btc-china
    huobi
    luno
    qryptos'''
