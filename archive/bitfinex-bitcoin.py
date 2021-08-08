#!/usr/bin/env python3
import urllib.request, json, datetime, time
from urllib.request import urlopen
from pathlib import Path

csv_file = Path(__file__).parents[0] / 'data' / 'bitcoin-bitfinex.csv'

def request(url):
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    print(data)

    return data['last_price'], data['low'], data['high'], data['volume'],

def main():
    current_time = datetime.datetime.now(datetime.timezone.utc)
    unix_timestamp = current_time.timestamp()
    print(int(unix_timestamp))

    url = 'https://api.bitfinex.com/v1/pubticker/btcusd'
    try:
        price, low, high, volume = request(url)
    except Exception as e:
        price, volume = None,None

    print('price: ' + str(price))
    print('volume: ' + str(volume))

    with open(csv_file, 'a') as f:
        f.write(str(int(unix_timestamp)) + ',' + str(price) + ',' + str(low) + ',' + str(high) + ',' + str(volume) + '\n')

if __name__ == '__main__':
    while True:
        now = datetime.datetime.now()
        while (now.second % 5):
            now = datetime.datetime.now()
            print(now.second)
            time.sleep(0.5)
        main()