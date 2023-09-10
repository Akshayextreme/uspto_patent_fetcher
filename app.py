import pandas as pd
import time
import requests
import sys


def get_uspto_link(start, rows, fromDate, toDate):
    return f"https://developer.uspto.gov/ibd-api/v1/application/grants?grantFromDate={fromDate}&grantToDate={toDate}&start={start}&rows={rows}&largeTextSearchFlag=N"


def get_api_resp(api):
    resp = requests.get(api)
    total_num = resp.json()['recordTotalQuantity']
    grants = pd.DataFrame(resp.json()['results'])
    grants = grants[['patentNumber', 'patentApplicationNumber', 'assigneeEntityName', 'filingDate', 'grantDate', 'inventionTitle']]
    time.sleep(1)
    return total_num, grants


def get_patents_between_dates(fromDate, toDate):
    total_grants, grants = get_api_resp(get_uspto_link(0, 1, fromDate, toDate))

    total_grants = 11
    rows = 3
    
    all_grants = []
    for start_num in range(0, total_grants, rows):
        num, grants = get_api_resp(get_uspto_link(start_num, rows, fromDate, toDate))
        all_grants.append(grants)
    df_grants = pd.concat(all_grants, axis=0, ignore_index=True)
    return df_grants


if __name__ == "__main__":

    patents = get_patents_between_dates(sys.argv[1], sys.argv[2])
    print(patents)