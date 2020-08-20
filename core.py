import json
import calendar
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from movingaverage import get200ma, get200ma_range
from tools import getCryptoId, convert_to_unix, convert_to_dt

crypto_id = getCryptoId()

with open('json/' + crypto_id  + '.json') as f:
  obj = json.load(f)

kl = list(obj.keys()) #keylist

pl = []

for k in kl:
  pl.append(obj[k][0]['price'])


printdebug = False

startdate = datetime(2016, 8, 8)
enddate = datetime(2020, 8, 1)


prices = kl[kl.index(str(convert_to_unix(startdate))):kl.index(str(convert_to_unix(enddate)))] #create a new list of unix-timestamps from startdate-enddate(+1)
price_at_start = obj[str(convert_to_unix(startdate))][0]['price'] #price at start
price_at_end = obj[str(convert_to_unix(enddate))][0]['price']     #price at end


tbuy = convert_to_unix(startdate + timedelta(hours=11, minutes=0))
tsell = convert_to_unix(startdate + timedelta(hours=8, minutes=0))


trepeat = 60*60*24  #when to repeat the buy/sell action; 86400 = one day, 604800 = one week etc.
budget = price_at_start        #starting budget to invest
#val = 0.0           #amount of cryptocurrency 

"""
for i in range(int(len(prices)/288)):
  plot_prices.append(obj[str(int(convert_to_unix(startdate))+(i*86400))][0]['price'])
"""

plot_prices = []
budget_list = []

#print(get200ma(convert_to_unix(datetime(2020, 1, 1)), pl, kl))

ma200 = get200ma_range(convert_to_unix(datetime(2020, 1, 2)), convert_to_unix(datetime(2020, 8, 18)), pl, kl)

print(ma200)
print(len(ma200))

ma200_days = []

for x in range(len(ma200)):
  pass

plt.plot(ma200)
plt.show()

"""
#plt.plot(plot_prices, label=crypto_id[:3] + "-Price")
#plt.plot(budget_list[0])
#plt.xlim(0, len(plot_prices))
plt.ylim(0)
plt.xlabel("Time")
plt.ylabel("Price")


days = convert_to_unix(enddate)-convert_to_unix(startdate)
days = days/60/60/24
years = days/365
months = days/30
win_factor = money/price_at_start
win_factor_expected = money/price_at_end

print("Starting price: ", price_at_start)
print("Ending price: ", price_at_end)
print()
print("Expected outcome: %.02f$" %(budget*(price_at_end/price_at_start)))
print("Budget after %i days (%0.2f years or %0.2f months): %0.2f$" %(days, years, months, money))
print("Gewinnfaktor insgesamt: %0.2f" %win_factor)
print("Gewinnfaktor (vgl hodl): %0.2f" %win_factor_expected)  #wie viel höher ist der gewinn, im vergleich mit der HODL strategie (einkauf beim start datum; verkauf beim enddatum)

plt.legend()
plt.show()

"""