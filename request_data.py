import requests
import json

#starting at 1514764800 (1.1.2018 0:00)
#steps of 4000 with 5min interval
#   ->       20000min with one request
# 20000*60 = 1.200.000 seconds per request
# 1577836800

starttime = 1388534400      #1.1.2014
max = 1596240000            #1.8.2020
limit = 4000

i = 0
c = limit*5*60  #constant which is added to utime after each run

utime=starttime
output = {}

while utime <= max:
    response = requests.get('https://api.coinpaprika.com/v1/tickers/btc-bitcoin/historical?start=' + str(utime) + '&limit=' + str(limit))
    res = json.loads(response.content)

    for x in range(len(res)):
        if(utime+5*60*x<max):
            output[utime+5*60*x] = []
            output[utime+5*60*x].append({
                #'timestamp': res[x]["timestamp"],
                #'unixtime': utime+5*60*x,
                'price': res[x]["price"]
            })
        else: 
            break

    utime += c
    i+=limit
    print(i/limit)

with open('temp.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)
