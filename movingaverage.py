#gibt zurück, ob das 50 Tage moving average über dem 200 Tage moving average ist.

debug_print = False

def is_goldencross(timestamp, price_list):
    return False

def get200ma(timestamp, price_list, key_list):
    total = 0
    daily = 0

    index = 0

    for day in range(200):    #last 200days
        for ts in range(288):    #every timestamp per day
            #daily += price_list[key_list.index(str(timestamp - (86400*day) - (300*ts)))]
            if day == 0:
                index = key_list.index(str(timestamp - (86400*day) - (300*ts)))
            daily += price_list[index-(day*ts)]
        #print("day %s avg: %0.2f" %(day, daily/288))
        total += daily/288 
        daily = 0

    return round(total/200, 2)

def getma_range(number_of_days, starttime, endtime, price_list, key_list):
    starttime = int(starttime)
    endtime = int(endtime)
    days = int((endtime - starttime) / 86400)
    index = key_list.index(str(starttime))
    decimals = len(str(price_list[0]).split('.')[1])
    daily = 0

    day_prices = []
    ma_total = []

    for x in range(days):
        if x == 0:
            #get price for last 200 days
            for day in range(number_of_days):    #last 200days
                #if debug_print:
                if debug_print:
                    print(index)
                    print(index-(day*288))
                    print("days: %s daily: %s " %(day, daily))
                if index-(day*288) > 0:
                    day_prices.append(round(price_list[index-(day*288)], 2))
                else:       #if the price data given has no data, append the price at the starting time to the list
                    day_prices.append(round(price_list[key_list.index(str(starttime))], 6))
            
            sum = 0


            #calculate 200 day average
            for x in range(len(day_prices)):
                sum += day_prices[x]

            if len(day_prices) != 0:
                total = sum/len(day_prices)
            else:
                total = price_list[key_list.index(str(starttime))]

            total = round(total, decimals)

            if debug_print: print(total)

            ma_total.append(total)
        else:
            if len(day_prices) > 0:
                day_prices.pop(0)    #remove first elemt from day_prices list
            daily = price_list[index+(x*288)]   #sucht den nächsten preis (24h später, 300s*288)
            day_prices.append(round(daily, decimals))   #append new day_price to list

            if debug_print: print("price today:%s " %daily)

            daily = 0
            sum = 0
            #calculate 200 day average
            for x in range(len(day_prices)):
                sum += day_prices[x]
 
            total = sum/len(day_prices)
            total = round(total, decimals)

            if debug_print: print(total)

            ma_total.append(total)
    return ma_total
