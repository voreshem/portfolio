import json
from urllib.request import urlopen

with urlopen("https://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json") as response:
    source = response.read()

data = json.loads(source)

usd_rates = dict()

for item in data['list']['resources']:
    name = item['resource']['fields']['name']
    price = item['resource']['fields']['price']
    usd_rates[name] = price

pair = input("Converts USD to other currencies!\n\nGive USD/x pair for conversion, e.g.: USD/EUR... \n").upper()
ammount = int(input("Give ammount... \n"))
converted = ammount * float(usd_rates[pair])

print(f"When converted, that comes to {round(converted, 2)} {pair[4:]}.")
