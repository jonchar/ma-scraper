#! /usr/bin/env python
#
# Script for scraping band names and basic associated information from
# http://www.metal-archives.com
#
# Author: Jon Charest (http://github.com/jonchar
# Year: 2016
#
# Approach:
# For each {NBR, A-Z}
# Read number of entries for given letter using result from `get_url`
# Determine how many requests of 500 entries are required, issue requests
# Read JSON in the `Requests` object returned by `get_url` using `r.json()`
# Read contents in 'aaData' key into a pandas `DataFrame`
# Set column names to `column_names`
# Clean up columns
# Concatenate & store outputs in a DataFrame
# Save final DataFrame to csv

import datetime
import requests
from pandas import DataFrame

BASEURL = 'http://www.metal-archives.com'
RELURL = '/browse/ajax-letter/json/1/l/'
response_len = 500

def get_url(letter='A', start=0, length=500):
    """Gets the listings displayed as alphabetical tables on M-A for input
    `letter`, starting at `start` and ending at `start` + `length`.
    Returns a `Response` object. Data can be accessed by callingt the `json()`
    method of the returned `Response` object."""
    
    payload = {'sEcho': 0,  # if not set, response text is not valid JSON
               'iDisplayStart': start,  # set start index of band names returned
               'iDisplayLength': length} # only response lengths of 500 work
    
    r = requests.get(BASEURL + RELURL + letter, params=payload)
    
    return r

# Data columns returned in the JSON object
column_names = ['NameLink', 'Country', 'Genre', 'Status']
data = DataFrame() # for collecting the results

# Valid inputs for the `letter` parameter of the URL are NBR or A through Z
letters = 'NBR A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
date_of_scraping = datetime.datetime.utcnow().strftime('%Y-%m-%d')

# Retrieve the data
for letter in letters:
    
    # Get total records for given letter & calculate number of chunks
    print('Current letter = ', letter)
    r = get_url(letter=letter, start=0, length=response_len)
    js = r.json()
    n_records = js['iTotalRecords']
    n_js_files = int(n_records / response_len) + 1
    print('Total records = ', n_records)
    
    # Retrieve chunks
    for i in range(n_js_files):
        start = response_len * i
        if start + response_len < n_records:
            end = start + response_len
        else:
            end = n_records
        print('Fetching band entries ', start, 'to ', end)
        
        for attempt in range(10):
            try:
                r = get_url(letter=letter, start=start, length=response_len)
                js = r.json()
                # Store response
                df = DataFrame(js['aaData'])
                data = data.append(df)
            # If the response fails, r.json() will raise an exception, so retry 
            except JSONDecodeError:
                print('JSONDecodeError on attempt ', attempt, ' of 10.')
                print('Retrying...')
                continue
            break

# Set informative names
data.columns = column_names

# Current index corresponds to index in smaller chunks concatenated
# Reset index to start at 0 and end at number of bands
data.index = range(len(data))

# Save to CSV
f_name = 'MA-band-names_{}.csv'.format(date_of_scraping)
print('Writing band data to csv file:', f_name)
data.to_csv(f_name)
print('Complete!')
