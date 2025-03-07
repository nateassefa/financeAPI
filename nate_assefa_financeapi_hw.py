# -*- coding: utf-8 -*-
"""Nate Assefa - FinanceAPI HW.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BF_k4lcdr-NZM8pWl2Fs0OPYftC8a39Q

# **Task 1**
"""

import json
import pandas as pd
import json
import requests

stocks = input("Enter stock symbols separated by commas: ").replace(" ", "")

apikey=""

url = "https://yfapi.net/v6/finance/quote"

querystring = {"symbols": stocks}

headers = {
    'x-api-key': apikey
    }

response = requests.request("GET", url, headers=headers, params=querystring)
print(json.dumps(response.json(), indent=4))

# Iterate through each row and print the required format
df = pd.DataFrame(response.json()['quoteResponse']['result'])
for index, row in df.iterrows():
    print(f"Stock Ticker: {row['symbol']}, Company: {row['displayName']}, Current Market Price: ${row['regularMarketPrice']:.2f}")

# Convert response to DataFrame
df = pd.DataFrame(response.json()['quoteResponse']['result'])
df.head()

"""# **Task 2**"""

module = input("Choose a module from the Quote Summary Endpoint ")

import requests
import json

apikey = ""
url = f"https://yfapi.net/v11/finance/quoteSummary/AAPL"

querystring = {
    "symbol": "AAPL",
    "modules": module
}

headers = {
    'x-api-key': apikey
}

#headers = {'Authorization': f'Bearer {apikey}'}


#response = requests.get(url, headers=headers, params=querystring)
response = requests.request("GET", url, headers=headers, params=querystring)


# Pretty print the JSON response
print(json.dumps(response.json(), indent=4))

# If module chosen is summaryDetail to retreive the 52 week high and low
if module == 'summaryDetail':

  data = response.json()['quoteSummary']['result'][0]['summaryDetail']
  low = data['fiftyTwoWeekLow']['raw']
  high = data['fiftyTwoWeekHigh']['raw']

  df = pd.DataFrame([{
      '52 Week Low': low,
      '52 Week High': high
  }])


# If module chosen is financial Data to retreive ROA
else:
  data = response.json()['quoteSummary']['result'][0]['financialData']
  roa = data['returnOnAssets']['raw']

  df = pd.DataFrame([{
      'Return on Assets': roa
  }])

df.head()

"""# **Task 2.2**"""

# Find trending stocks
import requests
import json

apikey = ""
url = "https://yfapi.net/v1/finance/trending/us"

# querystring = {
#     "symbol": "AAPL",
#     "modules": module
# }

headers = {
    'x-api-key': apikey
}




#response = requests.get(url, headers=headers, params=querystring)
response = requests.request("GET", url, headers=headers, params=querystring)
trendingStocks = response.json()['finance']['result'][0]['quotes']
symbols = []

for stock in trendingStocks:
  symbol = stock['symbol']

  quoteSummary = f"https://yfapi.net/v11/finance/quoteSummary/{symbol}"

  querystring = {
    "modules": "summaryDetail, price"
  }

  response = requests.request("GET", quoteSummary, headers=headers, params=querystring)
  stockData = response.json()['quoteSummary']['result'][0]

  # Extract the data
  price = stockData['price']['regularMarketPrice']['raw']
  actualName = stockData['price']['longName']
  fiftyTwoWeekLow = stockData['summaryDetail']['fiftyTwoWeekLow']['raw']
  fiftyTwoWeekHigh = stockData['summaryDetail']['fiftyTwoWeekHigh']['raw']

  symbols.append({
    'Ticker': symbol,
    'Actual Name': actualName,
    'Price': price,
    '52 Week Low': fiftyTwoWeekLow,
    '52 Week High': fiftyTwoWeekHigh
  })

  df = pd.DataFrame(symbols)
df.head()

