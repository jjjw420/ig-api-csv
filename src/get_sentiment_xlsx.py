"""
    Market sentiment to csv.

    Hannes Wagener - 2021
"""
import requests
import json
import sys
import datetime
import os.path
from openpyxl import load_workbook
from openpyxl import Workbook

IG_IDENTIFIER = "your IG user name"
IG_PASSWORD = "your IG password"
IG_API_KEY = "your IG API Key"


IG_API_BASE_URL = "https://api.ig.com/gateway/deal/"
IG_SENTIMENT_MARKETS = "EURGBP,EURUSD,EURAUD,EURCAD,EURCHF,EURNZD,EURJPY,GBPUSD,GBPAUD,GBPNZD,GBPCAD,GBPJPY,GBPCHF,AUDUSD,AUDNZD,AUDCAD,AUDCHF,AUDJPY,NZDCAD,NZDCHF,NZDJPY,NZDUSD,CADCHF,CADJPY,CHFJPY,USDJPY,USDCHF,USDCAD,USDSGD"

xslx_fields = ["Date", "Market", "Long Position %", "Short Position %"]
date_format = "%Y-%m-%d %H:%M:%S"
output_xlsx_file = "client_sentiment.xlsx"

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
client_sentiment_sheet = "Client Sentiment"
write_header = True
wb = None
ws = None
if os.path.exists(output_xlsx_file):
    write_header = False
    wb = load_workbook(output_xlsx_file)
    ws = wb.get_sheet_by_name(client_sentiment_sheet)
else:
    wb = Workbook()
    ws = wb.create_sheet(client_sentiment_sheet, 0) 
    ws['A1'] = xslx_fields[0]
    ws['B1'] = xslx_fields[1]
    ws['C1'] = xslx_fields[2]
    ws['D1'] = xslx_fields[3]


dte = datetime.datetime.now()
dte_str = dte.strftime(date_format)

i = 1
for client_sentiment in resp_obj["clientSentiments"]:
    client_sentiment["date"] = dte_str
    ws.insert_rows(2)
    ws['A2'] = client_sentiment["date"]
    ws['B2'] = client_sentiment["marketId"]
    ws['C2'] = client_sentiment["longPositionPercentage"]
    ws['D2'] = client_sentiment["shortPositionPercentage"]
    i = i + 1


s.close()
wb.save(output_xlsx_file)

print("Done! See: %s" % output_xlsx_file)