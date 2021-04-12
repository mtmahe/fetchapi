import requests
import json

from config import Config

# API info
api_key = Config.IEX_KEY
cm_key = Config.CM_KEY
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


# Iterate through Iex list and make api calls
responseDict = {}
for item in toGetIex:
    #response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{item}/quote?token={api_key}")
    response = requests.get(f"https://cloud.iexapis.com/stable/stock/{item}/quote?token={api_key}")
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

# Okay, now break it up
req_data = json.loads(jsonData)

keys = req_data.keys()
for key in keys:
    type = req_data[key]["type"]
    name = req_data[key]["name"]
    symbol = req_data[key]["symbol"]
    price = req_data[key]["price"]
    date = req_data[key]["date"]

#print(type,name,symbol,price,date)

# Post it
newHeaders = {'Content-type': 'application/json',
    'Authorization': cm_key,
    'Accept': 'text/plain'
    }
print("Uploading to server...")
response = requests.post('http://chezmahe.com/receive', data = jsonData, headers=newHeaders)

# Check response
if response.status_code == 200:
    print(response.content)
else:
    print('[?] Unexpected Error: [HTTP {0}]: Content {1}'.format(response.status_code, response.content))
