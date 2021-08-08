#!/usr/bin/env python3
'''
Cryptowat.ch API
https://cryptowat.ch/docs/api
https://api.cryptowat.ch/markets/prices '''

import urllib.request, json, datetime, time
from urllib.request import urlopen
from pathlib import Path

csv_file_price = Path(__file__).parents[0] / 'data' / 'cryptowatch-bitcoin-price2.csv'

def request(url):
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    print(data)

    return data['result']['price']['last'], data['result']['volume']

def main():
    current_time = datetime.datetime.now(datetime.timezone.utc)
    unix_timestamp = current_time.timestamp()
    print(int(unix_timestamp))

    url = 'https://api.cryptowat.ch/markets/prices'
    try:
        price, volume = request(url)
    except Exception as e:
        print(e)

    #with open(csv_file_price, 'a') as f:
     #   f.write(str(int(unix_timestamp)) + ',' + price + '\n')

if __name__ == '__main__':
    #main()
    while True:
        now = datetime.datetime.now()
        while (now.second % 5):
            now = datetime.datetime.now()
            print(now.second)
            time.sleep(0.5)
        main()
