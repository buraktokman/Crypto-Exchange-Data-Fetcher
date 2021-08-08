#!/usr/bin/env python3
'''
Cryptowat.ch API
https://cryptowat.ch/docs/api
https://api.cryptowat.ch/markets/gdax/btcusd/trades '''

import urllib.request, json, datetime, time
from pathlib import Path
from urllib.request import urlopen

exchanges = [
    'okex',
    'binance',
    'huobi'
    ]
pair = 'btcusdt'
limit = 0
since = 0
sleep_seconds = 60 * 60 * 1 # 1 hour
print_new_lines = False

def load_data(csv_file):
    print('loaded old data from csv file: ', end='')
    with open(csv_file, 'r') as f:
        lines = f.read().split('\n')
    print(len(lines))
    return lines

def request(url):
    global data
    print('downloading data')
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    print('fetched data size: ',end='')
    return data['result']

def new_items(lines_old,lines_new):
    print('selecting new items')
    temp = []
    if len(lines_old)-len(lines_new) < 0:
      go_back = 0
    else:
      go_back = len(lines_old)-len(lines_new)
    for x in range(len(lines_old) - 1,go_back,-1):
        if lines_new[0] == lines_old[x]:
            findex = x - 1
            for x in range(len(lines_old) - findex - 1,len(lines_new)):
                temp.append(lines_new[x])
            break
        elif x == go_back + 1:
            temp = lines_new
    return temp
    '''
def new_items(lines_old,lines_new):
    print('selecting new items')
    #temp = list(set(lines_old[1:]).symmetric_difference(lines_new))
    temp = []
    item_last = -1 * len(lines_new) + -1
    for x in lines_new:
        if x not in lines_old[item_last:]:
            temp.append(x)
    return temp'''

def fetch(exchange):
    print(exchange)
    url = 'https://api.cryptowat.ch/markets/' + exchange + '/' + pair + '/trades?limit=' + str(limit) +'&since=' + str(since)
    try:
        print('fetching data')
        data = request(url)
    except Exception as e:
        data = None
        print('unable to fetch ' + exchange)
        return

    lines_fetched = []
    for i in range(len(data)):
        line = ''
        for y in range(len(data[i])):
            if y == 0:
                line = str(data[i][y]) # format(price,'.3f')
            elif y == 1:
                line = line + ',' + str(data[i][y])
            elif y == 2:
                line = line + ',' + pair + ',' + str(data[i][y])
            elif y < len(data[i]):
                line = line + ',' + str('{0:f}'.format(data[i][3]))
        lines_fetched.append(line)
    print(len(lines_fetched))

    # Read data
    csv_file = Path(Path(__file__).parents[0] / 'data' / 'trade', exchange + '-' + pair + '-trade.csv')

    # Write to file
    lines_old = load_data(csv_file)

    # Find new data
    lines_new = new_items(lines_old, lines_fetched)
    if print_new_lines == True:
        for line in lines_new:
            print(line)
    print('new order count: ' + str(len(lines_new)))

    # Write new lines to file
    print('writing to csv file')
    with open(csv_file, 'a') as f:
        for x in lines_new:
            f.write(str(x) + '\n')

    # Clear the memory
    del lines_fetched[:]
    del lines_old[:]
    del lines_new[:]
    print('---')

def main():
    while True:
        for x in exchanges:
            fetch(x)
        print('sleeping for ' + str(sleep_seconds) + ' seconds')
        print('---')
        time.sleep(sleep_seconds)

if __name__ == '__main__':
    main()

    '''
    Exchanges that are not supported
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
