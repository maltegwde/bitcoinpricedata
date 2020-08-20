import json
from tools import getCryptoId

crypto_id = getCryptoId()

filename = "json/" + crypto_id + ".json"

with open(filename) as f:
  obj = json.load(f)

kl = list(obj.keys()) #keylist
output = {}

for i in range(len(kl)-1):
  tmp = int(kl[i]) + 300
  diff = int(kl[i+1]) - int(kl[i])

  if not diff == 300:   #if there is a gap in the data
    print("missing data at " + kl[i] + " | " + kl[i+1])
    d2 = int(diff / 300)
    d2 -= 1

    pdiff = obj[kl[i+1]][0]['price'] - obj[kl[i]][0]['price']
    pdiff = round(pdiff)

    pdiff_per_step = pdiff/d2

    utime = int(kl[i])
    price = round(obj[kl[i]][0]['price'], 2)

    for i in range(d2):
      utime+=300
      price += pdiff_per_step
      price = round(price, 2)

      output[str(utime)] = []
      output[str(utime)].append({
        'price': price
      })

merged = {**obj, **output}

with open(filename, 'w') as outfile:
    json.dump(merged, outfile, indent=4, sort_keys=True)
