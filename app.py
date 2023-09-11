import pandas as pd
import time
import requests
import os
import logging
import argparse

PAGE_SIZE = 100  # Adjust as needed

def get_uspto_link(start, rows, fromDate, toDate):
    """
    Function to generate dynamic API link with given from-to date and start record with pagenation number.

    Args:
        start (int): Starting record number
        rows (int): Specify number of rows to be returned, max returned by API is 100
        fromDate (str): Fetch patent granted onwards this date, date in YYYY-MM-DD format
        toDate (str): Fetch patent granted till this date, date in YYYY-MM-DD format

    Returns:
        str: API link
    """
    return f"https://developer.uspto.gov/ibd-api/v1/application/grants?grantFromDate={fromDate}&grantToDate={toDate}&start={start}&rows={rows}&largeTextSearchFlag=N"


def get_api_resp(api):
    """
    Function to get API response and to process it.

    Args:
        api (str): API link to fetch the patents from

    Returns:
        total_num (int): Total number of patents between given dates
        grants (pd.DataFrame): Fetch patents as pandas DataFrame

    Raises:
        RequestException: If GET fails and returns None
    """
    total_num, grants = None, None

    try:
        # GET USPTO API
        resp = requests.get(api)
        resp.raise_for_status()

        # get total number of granted patents
        total_num = resp.json().get('recordTotalQuantity')

        # get patent data
        grants = pd.DataFrame(resp.json().get('results'))
        grants = grants[['patentNumber', 'patentApplicationNumber', 'assigneeEntityName', 'filingDate', 'grantDate', 'inventionTitle']]
        
    except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            
    return total_num, grants


def get_patents_between_dates(fromDate, toDate):
    """
    Function to all granted patents between given dates.

    Args:
        fromDate (str): Fetch patent granted onwards this date, date in YYYY-MM-DD format
        toDate (str): Fetch patent granted till this date, date in YYYY-MM-DD format

    Returns:
        None
        Generates patents/patent_data.parquet file
    """
    # First call to get total number of patents between given dates.
    total_grants, grants = get_api_resp(get_uspto_link(0, 1, fromDate, toDate))
    logging.info(f"Total patents between {fromDate} - {toDate} are {total_grants}")

    all_grants = []
    total_fetched = 0

    # Sequentially fetch 100 patents by looping over total number of patents
    for start_num in range(0, total_grants, PAGE_SIZE):
        logging.info(f"Fetching started from {start_num}")
        num, grants = get_api_resp(get_uspto_link(start_num, PAGE_SIZE, fromDate, toDate))
        if grants is not None:
            all_grants.append(grants)
        total_fetched += len(grants)
        logging.info(f"Fetched {total_fetched}/{total_grants} patents")
    df_grants = pd.concat(all_grants, axis=0, ignore_index=True)
    logging.info(f"Fetched : {df_grants.shape} patents. END")
    return df_grants


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="USPTO Patent Fetcher")
    parser.add_argument("fromDate", help="Start date in YYYY-MM-DD format")
    parser.add_argument("toDate", help="End date in YYYY-MM-DD format")
    args = parser.parse_args()

    fromDate = args.fromDate
    toDate = args.toDate
    '''
    Some error handling needs to be done here for checking -
    1. Input date format
    2. fromDate < toDate
    Skipping because lack of time...
    '''

    # Create dir to store patent data
    if not os.path.exists("patents"):
        os.makedirs("patents")

    # Initialize logging
    logging.basicConfig(filename='patent_fetcher.log', level=logging.INFO)

    start_time = time.time()
    df_grants = get_patents_between_dates(fromDate, toDate)
    # Store patent data
    df_grants.to_parquet(os.path.join("patents", "patent_data.parquet"))
    logging.info(f"Total execution time: {(time.time() - start_time)/60.0:.2f} min")