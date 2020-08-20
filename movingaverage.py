#gibt zurück, ob das 50 Tage moving average über dem 200 Tage moving average ist.

def is_goldencross(number, price_list):


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

def get200ma_range(starttime, endtime, price_list, key_list):
    days = int((endtime - starttime) / 86400)
    index = key_list.index(str(starttime))
    daily = 0

    day_prices = []
    ma_total = []

    for x in range(days):
        if x == 0:
            #get price for last 200 days
            for day in range(200):    #last 200days
                daily = price_list[index-(day*288)]
                print(index)
                print(index-(day*288))
                print("days: %s daily: %s " %(day, daily))
                day_prices.append(round(daily, 2))
                daily = 0
            
            sum = 0
            #calculate 200 day average
            for x in range(len(day_prices)):
                sum += day_prices[x]

            total = sum/len(day_prices)


            total = round(total, 2)

            print(total)

            ma_total.append(total)
        else:
            day_prices.pop(0)    #remove first elemt from day_prices list
            daily = price_list[index+(x*288)]   #sucht den nächsten preis (24h später, 300s*288)
            day_prices.append(round(daily, 2))   #append new day_price to list
            print("price today:%s " %daily)
            daily = 0

            sum = 0
            #calculate 200 day average
            for x in range(len(day_prices)):
                sum += day_prices[x]

            total = sum/len(day_prices)
            total = round(total, 2)

            print(total)
            

            ma_total.append(total)
    return ma_total

def get50ma():
    pass