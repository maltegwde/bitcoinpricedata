import requests
import json
from json.decoder import JSONDecodeError
from datetime import datetime, timedelta
from tools import convert_to_unix, convert_to_dt
from config import getCryptoId

#starting at 1514764800 (1.1.2018 0:00)
#steps of 4000 with 5min interval
#   ->       20000min with one request
# 20000*60 = 1.200.000 seconds per request
# 1577836800

starttime = convert_to_unix(datetime(2013, 5, 1))
endtime = convert_to_unix(datetime(2020, 8, 23) + timedelta(minutes=5))
limit = 4000

crypto_id = getCryptoId()

filename = "json/" + crypto_id + ".json"

i = 0
c = limit*5*60  #constant which is added to utime after each run

utime=starttime
output = {}

url = 'https://api.coinpaprika.com/v1/tickers/' +  crypto_id + '/historical?start=' + str(utime) + '&limit=' + str(limit)

print(url)

while utime <= endtime:
    i+=limit
    response = requests.get(url)

    print("Statuscode: %s" % response.status_code)

    try:
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
    except Exception as e:
      print(e)
    
    print("Request number: %s" %(int(i/limit)))
    #print("lenres %s" %len(res))
    #print("Price at %s: %s " %(utime, res[utime+300]["price"]))


obj = output
kl = list(obj.keys()) #keylist

#with open('json/' + crypto_id + '.json', 'w') as outfile:
#    json.dump(output, outfile, indent=4)

missing_data = 0

print(str(obj[kl[0]][0]['price']).split('.')[1])
decimals = len(str(obj[kl[0]][0]['price']).split('.')[1])


for i in range(len(kl)-1):
  tmp = int(kl[i]) + 300
  diff = int(kl[i+1]) - int(kl[i])

  if not diff == 300:   #if there is a gap in the data
    print("missing data at %s | %s" % (kl[i], kl[i+1]))
    missing_data += 1
    d2 = int(diff / 300)
    d2 -= 1

    pdiff = obj[kl[i+1]][0]['price'] - obj[kl[i]][0]['price']
    pdiff = round(pdiff)

    pdiff_per_step = pdiff/d2

    utime = int(kl[i])
    price = obj[kl[i]][0]['price']

    for i in range(d2):
      utime+=300
      price += pdiff_per_step
      price = round(price, int(decimals))

      output[utime] = []
      output[utime].append({
        'price': price
      })

print("saving to file...")

merged = {**obj, **output}

percentage_of_missing_datapoints = 0

if missing_data > 0:
  percentage_of_missing_datapoints = (missing_data/len(kl)) * 100
  
with open(filename, 'w') as outfile:
    json.dump(merged, outfile, indent=4, sort_keys=True)

print()
print(decimals)
print("Fixed the price-file! %s datapoints were fixed. That's %0.2f%% of all %s datapoints" %(missing_data, percentage_of_missing_datapoints, len(kl)))

