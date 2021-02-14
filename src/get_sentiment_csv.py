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
from collections import OrderedDict 

# modify the following with your IG Credentials
IG_IDENTIFIER = "your IG user name"
IG_PASSWORD = "your IG password"
IG_API_KEY = "your IG API Key"

# the following list determines the order in the spreadsheet.  
# NOTE!! If this order changes - you must start a new sheet, however it is safe to append new markets at the end.
IG_SENTIMENT_MARKETS = "EURGBP,EURUSD,EURAUD,EURCAD,EURCHF,EURNZD,EURJPY,GBPUSD,GBPAUD,GBPNZD,GBPCAD,GBPJPY,GBPCHF,AUDUSD,AUDNZD,AUDCAD,AUDCHF,AUDJPY,NZDCAD,NZDCHF,NZDJPY,NZDUSD,CADCHF,CADJPY,CHFJPY,USDJPY,USDCHF,USDCAD,USDSGD"

IG_API_BASE_URL = "https://api.ig.com/gateway/deal/"
date_format = "%Y-%m-%d %H:%M:%S"
output_csv_file = "client_sentiment.csv"

csv_fields = ["Date"]
for k in IG_SENTIMENT_MARKETS.split(","):
    if k.strip() != "":
        csv_fields.append(k)    

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

# IG auth
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
# IG Sentiment API 
r = s.get(url=IG_API_BASE_URL + "clientsentiment", params={"marketIds": IG_SENTIMENT_MARKETS})

if r.status_code != 200:
    print("Error!")
    print("Status Code: %i" % r.status_code)
    print("Content: %s" % r.content)
    sys.exit(8)

print("Request Ok!")

resp_obj = json.loads(r.content)

write_header = True
if os.path.exists(output_csv_file):
    write_header = False

print("Writing csv...")
csv_f = open(output_csv_file, "a")
csv_w = csv.DictWriter(csv_f, fieldnames=csv_fields, quoting=csv.QUOTE_NONNUMERIC)
if write_header:
    csv_w.writeheader()

dte = datetime.datetime.now()
dte_str = dte.strftime(date_format)

if len(resp_obj) > 0:
    csv_row = {}
    csv_row["Date"] = dte_str
    for client_sentiment in resp_obj["clientSentiments"]:
        csv_row[client_sentiment["marketId"]] = client_sentiment["longPositionPercentage"]
        
    csv_w.writerow(csv_row)

#close session
s.close()
#close csv
csv_f.close()

print("Done! See: %s" % output_csv_file)