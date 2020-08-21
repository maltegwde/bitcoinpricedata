import json
from config import getCryptoId

crypto_id = getCryptoId()

filename = "json/" + crypto_id + ".json"

with open(filename) as f:
  obj = json.load(f)
  print(obj)

kl = list(obj.keys()) #keylist
output = {}

missing_data = 0

print(len(str(obj[kl[0]][0]['price'])))
decimals = len(str(obj[kl[0]][0]['price']).split('.')[1])


for i in range(len(kl)-1):
  tmp = int(kl[i]) + 300
  diff = int(kl[i+1]) - int(kl[i])

  if not diff == 300:   #if there is a gap in the data
    print("missing data at " + kl[i] + " | " + kl[i+1])
    missing_data += 1
    d2 = int(diff / 300)
    d2 -= 1

    pdiff = obj[kl[i+1]][0]['price'] - obj[kl[i]][0]['price']
    pdiff = round(pdiff)

    pdiff_per_step = pdiff/d2

    utime = int(kl[i])
    price = obj[kl[i]][0]['price']

    for i in range(d2):
      utime+=300
      price += pdiff_per_step
      price = round(price, int(decimals))

      output[str(utime)] = []
      output[str(utime)].append({
        'price': price
      })

print("saving to file...")

percentage_of_missing_datapoints = 0

if missing_data > 0:
  merged = {**obj, **output}
  with open(filename, 'w') as outfile:
    json.dump(merged, outfile, indent=4, sort_keys=True)
  percentage_of_missing_datapoints = (missing_data/len(kl)) * 100

print()
print(decimals)
print("Fixed the price-file! %s datapoints were fixed. That's %0.2f%% of all %s datapoints" %(missing_data, percentage_of_missing_datapoints, len(kl)))
