# Metal Archives Scraper

URL: http://www.metal-archives.com/

This script uses requests to retrieve the data and pandas to collect it before
saving in \*.csv format.

## Scraping band names alphabetically

Band names can be found alphabetically on the site. The tables they are
presented in are loaded via AJAX requests that return data in JSON format.
The script `MA_scraper.py` retrieves the alphabetical list of band names
along with the other information in the table (Country, Genre, & Status).

* The maximum number of band names returned is 500, it can be set by
`iDisplayLength`.

* The starting point in the alphabetical list for a given letter is set by
`iDisplayStart`.

* Every JSON response contains a field `sEcho`, which if left blank in the URL
request will result in invalid JSON being returned, so `sEcho` is set to 0 in
order to avoid this.

## Approach

The script collects the data in chunks of 500 bands at a time starting with
bands whose names start with a number and then alphabetically. If the response
does not contain valid JSON, the script will retry up to 10 times.

## Output

The collected information is then stored in a \*.csv file with the following
column headers and data types:

* `'NameLink'`: HTML snippet containing band name and link to corresponding
band page on Metal Archives (HTML string)

* `'Country'`: Country of origin (string)

* `'Genre'`: Description of band genre (string, terms not standardized)

* `'Status'`: HTML snippet describing band status (HTML string, active / split-up / changed
name / on hold / unknown / disputed)

Total number of bands may vary as the site is regularly updated.
Check [their stats page](http://www.metal-archives.com/stats) for a current
number.
