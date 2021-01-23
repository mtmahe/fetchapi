import requests
import json

from config import Config

# API info
api_key = Config.IEX_KEY
symbol = "AAPL"

# Make a list of desired iex items
toGetIex = [
    "AAPL",
    "BAC",
    "GM",
    "GE",
    "COKE",
    "MSFT",
    "AMZN",
    "TSLA",
    "TSM",
    "MA",
    "NVDA",
    "PYPL",
    "INTC",
    "NFLX",
    "CRM"
]

# Make API call
# response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{symbol}/quote?token={api_key}")
# response.raise_for_status()

# quote = response.json()

# Clean up the response
#data = {
#    "name": quote["companyName"],
#    "price": float(quote["latestPrice"]),
#    "symbol": quote["symbol"],
#    "volume": float(quote["iexVolume"])
#}

# Iterate through Iex list and make api calls
responseDict = {}
for item in toGetIex:
    response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{item}/quote?token={api_key}")
    response.raise_for_status()
    quote = response.json()

    # Update dict with new response item
    responseDict.update({item: {
        "type": "iex",
        "name": quote["companyName"],
        "symbol": item,
        "price": float(quote["latestPrice"]),
        "date": quote["latestTime"]
    }})

print(responseDict)

# Convert to json
jsonData = json.dumps(responseDict)

# Okay, now what does server need to do to break it up?
req_data = json.loads(jsonData)
#keys = newData.keys()
#for key in keys:
#    print(newData[key]["symbol"], newData[key]["date"])

keys = req_data.keys()
for key in keys:
    type = req_data[key]["type"]
    name = req_data[key]["name"]
    symbol = req_data[key]["symbol"]
    price = req_data[key]["price"]
    date = req_data[key]["date"]

print(type,name,symbol,price,date)


# Convert to json
# jsonData = json.dumps(data)

# Post it
newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

response = requests.post('http://test.chezmahe.com/receive', data = jsonData, headers=newHeaders)

print(response)
