import json
import calendar
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

crypto_id = "eth-ethereum"

with open('json/' + crypto_id  + '.json') as f:
  obj = json.load(f)

kl = list(obj.keys()) #keylist

printdebug = False
plot_pricesDone = False

startdate = datetime(2016, 8, 8)
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
        budget_list.append([])
        budget_list[num].append(money)
      elif num != 0:
        budget_list[num].append(money)
      val = money/price
      money = 0
      buy_time += trepeat
      if printdebug: 
        print("Bought at ", price)
        print("MONEY: " + str(money))
        print("VAL: " + str(val))
        print("time " + str(utime))
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
          print("VAL: " + str(val))
          print("time " + str(utime))

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
    print(a)
    for b in range(1, 24):
      tbuy = convert_to_unix(startdate + timedelta(hours=a))
      tsell = convert_to_unix(startdate + timedelta(hours=b))
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
 
  for a in range(5):
      tbuy = convert_to_unix(startdate + timedelta(hours=a+9))
      tsell = convert_to_unix(startdate + timedelta(hours=8))
      money = simulation(tbuy, tsell, budget, a)
      plt.plot(budget_list[a], label="Buy-Time:" + str(a+9))
      if money > max_money:
        max_money = money
        #max_val = str(a)+ " | " + str(b)

      if printdebug: 
        print("Max: %0.2f " %max_money)
        print(max_val)

  #print(max_val)
  return max_money

def crossed_Line(p1, p2, fibolist):
  for f in fibolist:
    if f > p1 and f < p2: #crossed from below
      return 1
    elif f < p1 and f > p2: #crossed from top
      return 2
  return 0


def fibonacci_retracement(time_start, time_end):
  timespan = kl[kl.index(str(time_start)):kl.index(str(time_end))]

  ascending = True

  max_price = 0
  low_price = 10000000

  max_time = 0
  low_time = 0

  #find highest and lowest price
  for utime in timespan:
    price = obj[utime][0]['price']
    plot_prices.append(price)
    if price > max_price: 
      max_price = price
      max_time = utime
    if price < low_price:
      low_price = price
      low_time = utime

  if low_time > max_time:
    ascending = False

  price_diff = max_price - low_price

  fibonacci_nums = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]

  price_nums = []

  colors = ['r', 'g', 'b']
  color_num = 0

  for fn in fibonacci_nums:
    tmp = round((low_price + price_diff * fn), 2)
    plt.axhline(y = tmp, color=colors[color_num], linestyle='-')
    color_num += 1
    color_num = color_num % len(colors)
    price_nums.append(tmp)
    
  if printdebug:
    print(price_nums)
    print("Max: %s at %s" %(max_price, str(convert_to_dt(int(max_time)))))
    print("Min: %s at %s" %(low_price, str(convert_to_dt(int(low_time)))))

  val = 1
  money = 0

  buy_in = obj[timespan[0]][0]['price']

  print(buy_in)

  for i in range(1, len(timespan)-1):
    utime_old = timespan[i-1]
    utime = timespan[i]
    price_old = obj[utime_old][0]['price']
    price = obj[utime][0]['price']
    if crossed_Line(price_old, price, price_nums) == 1:
      if val == 0 and money != 0:    #kauf den scheiß
        val = money/price
        money = 0
        #print(val)
        #print("bought at %s " %money)
        #print(money)
    elif crossed_Line(price_old, price, price_nums) == 2:
      if val != 0 and money == 0: #verkauf 
        money = price
        val = 0
        #print("sold at %s " %money)
        #print("value: %s" %pri)
        print(money)

  if val != 0:
    money = price
    val = 0

  hodl_faktor = obj[timespan[-1]][0]['price']/obj[timespan[0]][0]['price']
  print("Gewinnfaktor HODL: %s" %hodl_faktor)
  print("Gewinnfaktor %s " %(money/buy_in))

prices = kl[kl.index(str(convert_to_unix(startdate))):kl.index(str(convert_to_unix(enddate)))] #create a new list of unix-timestamps from startdate-enddate(+1)
price_at_start = obj[str(convert_to_unix(startdate))][0]['price'] #price at start
price_at_end = obj[str(convert_to_unix(enddate))][0]['price']     #price at end


tbuy = convert_to_unix(startdate + timedelta(hours=11, minutes=0))
tsell = convert_to_unix(startdate + timedelta(hours=8, minutes=0))

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
#money = multi_simulation()
#money = multi_simulation_graph()

fibo_start = datetime(2016, 12, 1)
fibo_end = datetime(2018, 1, 31)

#fibonacci_retracement(convert_to_unix(fibo_start), convert_to_unix(fibo_end))



plt.plot(plot_prices, label=crypto_id[:3] + "-Price")


#plt.plot(budget_list[0])
#plt.xlim(0, len(plot_prices))
#plt.ylim(0)
plt.xlabel("Time")
plt.ylabel("Price")
plt.show()

"""

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