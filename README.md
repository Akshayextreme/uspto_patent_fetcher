# USPTO Patent Fetcher

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