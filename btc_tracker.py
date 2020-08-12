import json
import calendar
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

with open('json/btc.json') as f:
  obj = json.load(f)

kl = list(obj.keys()) #keylist

printdebug = False
plot_pricesDone = False

startdate = datetime(2014, 1, 1)
enddate = datetime(2020, 8, 1)

#TODO: make budget list 2d list and create multiple graphs for each simulation

def convert_to_dt(timestamp):
  return datetime.utcfromtimestamp(timestamp)

def convert_to_unix(dt_obj):
  return calendar.timegm(dt_obj.timetuple())

def simulation(buy_time, sell_time, money, num):
  global plot_pricesDone
  val = 1234567

  #buy_time = convert_to_unix(startdate + timedelta(hours=18))
  #sell_time = convert_to_unix(startdate + timedelta(hours=10))

  if num != 0:
    budget_list.append([])
  for utime in prices:
    #print("t: %s  kl: %s" %(utime, kl[]))
    if str(utime) == str(buy_time):
      #buy btc
      price = obj[utime][0]['price']
      if num == 0 and not plot_pricesDone:
        plot_prices.append(price)
      elif num != 0:
        budget_list[num].append(money)
      val = money/price
      money = 0
      buy_time += trepeat
      if printdebug: 
        print("Bought at ", price)
        print("MONEY: " + str(money))
        print("VAL: " + str(val))
    elif str(utime) == str(sell_time):
      sell_time += trepeat
      if val != 1234567:
        #sell
        price = obj[utime][0]['price']
        money = val*price
        val = 0
        if printdebug: 
          print("Sold at ", price)
          print()
          print("MONEY: " + str(money))
          print("VAL: " + str(val))#

  plot_pricesDone = True
  #print()
  #print("Finished with: %0.2f" %money)
  if money == 0:
    money = val*price
    val = 0

  return money

def multi_simulation():
  max_money = 0
  max_val = ""

  #limit = 8
  for a in range(1, 24):
    for b in range(1, 24):
      tbuy = convert_to_unix(startdate + timedelta(hours=b))
      tsell = convert_to_unix(startdate + timedelta(hours=a))
      money = simulation(tbuy, tsell, budget, 0)
      if money > max_money:
        max_money = money
        max_val = str(a)+ " | " + str(b)

      if printdebug: 
        print("Max: %0.2f " %max_money)
        print(max_val)

  print(max_val)
  return max_money

def multi_simulation_graph():
  max_money = 0
  max_val = ""
 
  for a in range(4):
      tbuy = convert_to_unix(startdate + timedelta(hours=a+5))
      tsell = convert_to_unix(startdate + timedelta(hours=23))
      money = simulation(tbuy, tsell, budget, a)
      plt.plot(budget_list[a], label="Buy-Time:" + str(a+5))
      if money > max_money:
        max_money = money
        #max_val = str(a)+ " | " + str(b)

      if printdebug: 
        print("Max: %0.2f " %max_money)
        print(max_val)

  #print(max_val)
  return max_money



prices = kl[kl.index(str(convert_to_unix(startdate))):kl.index(str(convert_to_unix(enddate)))+1] #create a new list of unix-timestamps from startdate-enddate(+1)
price_at_start = obj[str(convert_to_unix(startdate))][0]['price'] #price at start
price_at_end = obj[str(convert_to_unix(enddate))][0]['price']     #price at end

tbuy = convert_to_unix(startdate + timedelta(hours=5, minutes=0))
tsell = convert_to_unix(startdate + timedelta(hours=23, minutes=0))

days = convert_to_unix(enddate)-convert_to_unix(startdate)
days = days/60/60/24


trepeat = 60*60*24  #when to repeat the buy/sell action; 86400 = one day, 604800 = one week etc.
budget = price_at_start        #starting budget to invest
#val = 0.0           #amount of cryptocurrency 

"""
for i in range(int(len(prices)/288)):
  plot_prices.append(obj[str(int(convert_to_unix(startdate))+(i*86400))][0]['price'])
"""

plot_prices = []
budget_list = []
#money = simulation(tbuy, tsell, budget, 0)
money = multi_simulation()

plt.plot(plot_prices, label="BTC-Price")
#plt.plot(budget_list[0])
#plt.xlim(0, len(plot_prices))
plt.ylim(0)
plt.xlabel("Time")
plt.ylabel("Price")

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