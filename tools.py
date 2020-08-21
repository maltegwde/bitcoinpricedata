from datetime import datetime
import calendar

def convert_to_dt(timestamp):
  return datetime.utcfromtimestamp(timestamp)

def convert_to_unix(dt_obj):
  return calendar.timegm(dt_obj.timetuple())

def getDailyPrices(startday, endday, price_list, key_list):
  daily_prices = []

  index = key_list.index(startday)

  tmp = startday

  while tmp < endday:
    daily_prices.append(price_list[index])
    index += 288

  if len(daily_prices) == 0:
    return 1
  return daily_prices