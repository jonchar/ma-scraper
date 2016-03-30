import datetime
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASEURL = 'http://www.metal-archives.com'
RELURL = '/browse/ajax-letter/json/1/l/'
response_len = 500

def get_url(letter='A', start=0, length=response_len):
    payload = {'sEcho': 0,
               'iDisplayStart': start,
               'iDisplayLength': length}
    r = requests.get(BASEURL + RELURL + letter, params=payload)
    return r

column_names = ['NameLink', 'Country', 'Genre', 'Status']

letters = 'NBR A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()

data = pd.DataFrame()

date_of_parsing = datetime.datetime.utcnow().strftime('%Y-%m-%d')

for letter in letters:
    print('Current letter = ', letter)
    r = get_url(letter=letter, start=0, length=response_len)
    js = r.json()
    n_records = js['iTotalRecords']
    n_js_files = int(n_records / response_len) + 1
    print('Total records = ', n_records)
    for i in range(n_js_files):
        start = response_len * i
        if start + response_len < n_records:
            end = start + response_len
        else:
            end = n_records
        print('Fetching records ', start, 'to ', end)
        for attempt in range(10):
            try:
                r = get_url(letter=letter, start=start, length=response_len)
                js = r.json()
                df = pd.DataFrame(js['aaData'])
                data = data.append(df)
            except JSONDecodeError:
                print('JSONDecodeError on attempt ', attempt, ' of 10.')
                print('Retrying...')
                continue
            break

data.columns = column_names
print('Writing data to csv...')
data.to_csv('MA-band-names_' + date_of_parsing + '.csv')
print('Complete!')
# Approach:
# For each {NBR, A-Z}
# Read number of entries for given letter using result from `get_url`
# Determine how many requests of 200 entries are required, issue requests
# Read JSON as returned by `get_url` using `json.loads`
# Read contents in 'aaData' key using `pd.DataFrame`
# Set column names using `column_names` from above
# Clean up columns
# Concatenate & store outputs in a DataFrame

