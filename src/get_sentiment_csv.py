"""
    Market sentiment to csv.

    Hannes Wagener - 2021
"""
import requests
import json
import csv
import sys
import datetime
import os.path

IG_IDENTIFIER = "your IG user name"
IG_PASSWORD = "your IG password"
IG_API_KEY = "your IG API Key"

IG_API_BASE_URL = "https://api.ig.com/gateway/deal/"
IG_SENTIMENT_MARKETS = "EURGBP,EURUSD,EURAUD,EURCAD,EURCHF,EURNZD,EURJPY,GBPUSD,GBPAUD,GBPNZD,GBPCAD,GBPJPY,GBPCHF,AUDUSD,AUDNZD,AUDCAD,AUDCHF,AUDJPY,NZDCAD,NZDCHF,NZDJPY,NZDUSD,CADCHF,CADJPY,CHFJPY,USDJPY,USDCHF,USDCAD,USDSGD"

csv_fields = ["date", "marketId", "longPositionPercentage", "shortPositionPercentage"]
date_format = "%Y-%m-%d %H:%M:%S"
output_csv_file = "client_sentiment.csv"

headers = {
    "Content-Type": "application/json", 
    "Accept": "application/json", 
    "X-IG-API-KEY": IG_API_KEY, 
    "Version": "2"
}

auth_body = {
    "identifier": IG_IDENTIFIER,
    "password": IG_PASSWORD,
    "encryptedPassword": None
}

s = requests.session()

#auth
print("Authenticating...")
s.headers.update(headers)
r = s.post(url=IG_API_BASE_URL + "session", json=auth_body)

if r.status_code != 200:
    print("Authentication failed!")
    print("Status Code: %i" % r.status_code)
    print("Content: %s" % r.content)
    sys.exit(8)

print("Authentication Successfull!")

s.headers.update({
    "CST": r.headers["CST"], 
    "X-SECURITY-TOKEN": r.headers["X-SECURITY-TOKEN"]
})

print("Getting Market Sentiment for %s" % (IG_SENTIMENT_MARKETS))

r = s.get(url=IG_API_BASE_URL + "clientsentiment", params={"marketIds": IG_SENTIMENT_MARKETS})

if r.status_code != 200:
    print("Error!")
    print("Status Code: %i" % r.status_code)
    print("Content: %s" % r.content)
    sys.exit(8)

print("Request Ok!")

resp_obj = json.loads(r.content)

s.close()

write_header = True
if os.path.exists(output_csv_file):
    write_header = False

print("Writing csv...")
csv_f = open(output_csv_file, "a")
csv_w = csv.DictWriter(csv_f, fieldnames=csv_fields, quoting=csv.QUOTE_ALL)
if write_header:
    csv_w.writeheader()

dte = datetime.datetime.now()
dte_str = dte.strftime(date_format)

for client_sentiment in resp_obj["clientSentiments"]:
    client_sentiment["date"] = dte_str
    csv_w.writerow(client_sentiment)

s.close()
csv_f.close()
print("Done! See: %s" % output_csv_file)