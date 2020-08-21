#this file in for various parameters

from datetime import datetime
from tools import convert_to_unix, convert_to_dt

debug_print = False
crpyto_id = "btc-bitcoin"
startdate = datetime(2015, 6, 4)
enddate = datetime(2019, 8, 19)

def getDebug_print():
    return debug_print

def getCryptoId():
    return crpyto_id

def getStart_date(fts): #fts = first timestamp 
    global startdate 
    if convert_to_unix(startdate) < int(fts): #if the chosen startdate timestamp is smaller than the first timestamp of the data, set it to the fts
        startdate = fts
    return str(convert_to_unix(startdate))

def getEnd_date(lts):   #lts = last timestamp
    global enddate
    if convert_to_unix(enddate) > int(lts):   #if the chosen enddate timestamp is bigger than the last timestamp of the data, set it to the lts
        enddate = lts
    return str(convert_to_unix(enddate))
