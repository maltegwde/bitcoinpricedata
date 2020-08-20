from datetime import datetime
import calendar

crypto_id = "btc-bitcoin"

def convert_to_dt(timestamp):
  return datetime.utcfromtimestamp(timestamp)

def convert_to_unix(dt_obj):
  return calendar.timegm(dt_obj.timetuple())

def getCryptoId():
  return crypto_id

def getDailyPrices(startday, endday):
  daily_prices = []

  tmp = startday

  while tmp < endday:
