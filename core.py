import json
import calendar
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from movingaverage import get200ma, get200ma_range, get50ma_range, getma_range
from tools import convert_to_unix, convert_to_dt, getDailyPrices
from config import getDebug_print, getCryptoId, getStart_date, getEnd_date

#read from config file
debug_print = getDebug_print()
crypto_id = getCryptoId()

#Open json file
print("open json file.")
with open('json/' + crypto_id  + '.json') as f:
  obj = json.load(f)
print("finshed reading json")

#retrieve info from the json object
kl = list(obj.keys()) #keylist - list of unix-timestamps, which are required to access the price-date with obj[UNIX][0]['price']
fts = kl[0]           #first timestamp
lts = kl[-1]          #last timestamp
startdate = getStart_date(fts)  #get startdate
enddate = getEnd_date(lts)      #get enddate
print(isinstance(startdate, str))
print(isinstance(enddate, str))
fp = obj[startdate][0]['price'] #first price
lp = obj[enddate][0]['price']   #last price



print("First timestamp of data: %s  |  %s  |  %s" %(fts, convert_to_dt(int(fts)), fp))
print("Last timestamp of data:  %s  |  %s  |  %s" %(lts, convert_to_dt(int(lts)), lp))

#create a pricelist from all data
price_list = []
for k in kl:
  price_list.append(obj[k][0]['price'])

#create a price_list from startdate to enddate used for graph
price_list_se = []
tmp = int(startdate)
while int(tmp) < int(enddate):
  price_list_se.append(obj[str(tmp)][0]['price'])
  tmp += 86400

#create a new list of unix-timestamps from startdate to enddate
prices = kl[kl.index(str(startdate)):kl.index(str(enddate))]

#create lists of movingaverage and plot them
ma_days = [50, 200]
for day in ma_days:
  plt.plot(getma_range(day, startdate, enddate, price_list, kl), label= str(day) + " day ma")
plt.plot(price_list_se, label=crypto_id)

#settings for matplotlib
plt.xlabel("Time")
plt.ylabel("Price")
plt.xlim(0, len(price_list_se))
plt.ylim(0)
plt.legend()
plt.show()