# ig-api-csv
# IG Trading API to CSV.

`get_sentiment_csv.py` fetches IG client sentiment data and appends it to a csv file.
`get_sentiment_xlsx.py` fetches IG client sentiment data and prepends it to a xlsx file.

Check each script to populate your IG credentials and the markets to fetch sentiment for.

# Requirements
- Python3 - See https://www.python.org/downloads/
- Python requests: See https://requests.readthedocs.io/en/latest/user/install/#install
- IG Account: you must have a valid IG account and API key.  See: https://labs.ig.com/gettingstarted
- openpyxl:  Required for excel file creation.  https://openpyxl.readthedocs.io/en/stable/

# Running
- Edit the `get_sentiment_csv.py` or `get_sentiment_xlsx.py` script file.  Populate your IG credentials(IG_IDENTIFIER, IG_PASSWORD) and the IG API key(IG_API_KEY) and save the file.
- run either `get_sentiment_csv.py` or `get_sentiment_xlsx.py` script (eg. python get_sentiment_csv.py)



