# USPTO Patent Fetcher Tech Test

## Description

Your task is to create a CLI program that calls the USPTO's API and saves patent
data for all granted patents granted between two dates provided as CLI arguments.

You can find documentation for the USPTO API here:
https://developer.uspto.gov/api-catalog/bulk-search-and-download

This is an example API request as a curl request
```
curl -X GET \
    --header 'Accept: application/json' \
    'https://developer.uspto.gov/ibd-api/v1/application/grants?grantFromDate=2017-01-01&grantToDate=2017-01-03&start=0&rows=100&largeTextSearchFlag=N' \
    | gunzip > output.json
```

What data you save from the API response and where/how you persist this data is up to
you, but as a minimum we would like you to save these attributes.
- patentNumber
- patentApplicationNumber
- assigneeEntityName
- filingDate
- grantDate
- inventionTitle

## Solution 1
```
1. app.py - Core logic
2. test.py -  unittest cases
3. Dockerfile
4. requirement.txt
```

```
Due to SSL certificate issues I couldn't get Docker container running.
```

### Steps to run
```
1. Install dependencies using requirements.txt
2. python3 -m unittest test.py
3. python3 app.py 2017-01-01 2017-01-03
4. Output -> patents/patent_data.parquet
5. Logfile -> patent_fetcher.log
6. Total execution time: 2.47 min
```

## Solution 2
```
Trying to reduce execution time by using asyncio library
```
### Steps to run
```
1. Install dependencies using requirements.txt
2. python3 app2.py 2017-01-01 2017-01-03
3. Output -> patents/split_<uuid>.parquet
4. Logfile -> patent_fetcher2.log
5. Total execution time: 1.22 min
```
