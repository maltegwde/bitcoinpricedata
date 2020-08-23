from datetime import datetime
import calendar

def convert_to_dt(timestamp):
  return datetime.utcfromtimestamp(timestamp)

def convert_to_unix(dt_obj):
  return calendar.timegm(dt_obj.timetuple())
