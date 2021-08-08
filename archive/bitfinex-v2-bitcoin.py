#!/usr/bin/env python3
'''
Bitfinex V2 API
https://docs.bitfinex.com/v2/reference#rest-public-ticker

FRR         float   Flash Return Rate - average of all fixed rate funding over the last hour
BID         float   Price of last highest bid
BID_PERIOD  int     Bid period covered in days
BID_SIZE    float   Size of the last highest bid
ASK         float   Price of last lowest ask
ASK_PERIOD  int     Ask period covered in days
ASK_SIZE    float   Size of the last lowest ask
DAILY_CHANGE    float   Amount that the last price has changed since yesterday
DAILY_CHANGE_PERC   float   Amount that the price has changed expressed in percentage terms
LAST_PRICE  float   Price of the last trade
VOLUME      float   Daily volume
HIGH        float   Daily high
LOW         float   Daily low '''

import urllib.request, json, datetime, time
from urllib.request import urlopen
from pathlib import Path

csv_file = Path(__file__).parents[0] / 'data' / 'bitfinex-bitcoin-price.csv'

def request(url):
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    print(data)
    return data[6],data[7],data[8],data[9]

def fetch():
    current_time = datetime.datetime.now(datetime.timezone.utc)
    unix_timestamp = current_time.timestamp()
    print(int(unix_timestamp))

    url = 'https://api.bitfinex.com/v2/ticker/tBTCUSD'
    try:
        price, volume, high, low = request(url)
    except Exception as e:
        price, volume, high, low = None,None,None,None
        print(e)

    print('price: ' + str(price))
    print('volume: ' + str(volume))
    print('high: ' + str(high))
    print('low: ' + str(low))

    with open(csv_file, 'a') as f:
        f.write(str(int(unix_timestamp)) + ',' + str(price) + ',' + str(low) + ',' + str(high) + ',' + str(volume) + '\n')

def main():
    while True:
        now = datetime.datetime.now()
        while (now.second % 5):
            now = datetime.datetime.now()
            print(now.second)
            time.sleep(0.5)
        fetch()

if __name__ == '__main__':
    main()