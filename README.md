# Metal Archives Scraper

URL: http://www.metalarchives.com/

Use requests to get URLs, Beautiful soup to parse the output.

## Scrape all band names

Band names can be found alphabetically on the site. The table they are
presented in are loaded via AJAX requests that return JSON.

* The maximum number of band names returned is 200, it can be set by
`iDisplayLength`.

* The starting point in the list for a given letter is set by `iDisplayStart`.

* Every JSON response contains a field `sEcho`, which if left blank in the URL
request will result in invalid JSON being returned, so `sEcho` should be set
to zero (or at least not left out of the request URL).
