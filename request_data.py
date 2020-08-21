import requests
import json
from datetime import datetime, timedelta
from tools import convert_to_unix, convert_to_dt
from config import getCryptoId

#starting at 1514764800 (1.1.2018 0:00)
#steps of 4000 with 5min interval
#   ->       20000min with one request
# 20000*60 = 1.200.000 seconds per request
# 1577836800

starttime = convert_to_unix(datetime(2014, 6, 1))
endtime = convert_to_unix(datetime(2020, 8, 19) + timedelta(minutes=5))
limit = 4000

i = 0
c = limit*5*60  #constant which is added to utime after each run

utime=starttime
output = {}

crypto_id = getCryptoId()
url = 'https://api.coinpaprika.com/v1/tickers/' +  crypto_id + '/historical?start=' + str(utime) + '&limit=' + str(limit)


while utime <= endtime:
    response = requests.get(url)
    res = json.loads(response.content)

    for x in range(len(res)):
        if(utime+5*60*x<endtime):
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
    print(int(i/limit))

print(output)

with open('json/' + crypto_id + '.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)
