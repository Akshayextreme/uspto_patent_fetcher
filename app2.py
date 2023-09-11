import aiohttp
import asyncio
import logging
import pandas as pd
import requests
import time
import uuid
import argparse
import os


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


def get_total_patent_count(api):
    """
    Function to get total number of granted patents.

    Args:
        api (str): API link to fetch the patents from

    Returns:
        total_num (int): Total number of patents between given dates

    Raises:
        RequestException: If GET fails and returns None
    """
    total_num = None
    try:
        resp = requests.get(api)
        resp.raise_for_status()
        total_num = resp.json()['recordTotalQuantity']
    except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
    return total_num


def patent_processor(result):
    """
    Function to process API response.

    Args:
        result (dict): Response from GET to API

    Returns:
        None
        Generates patent chunk files at patents/split_<>.parquet
    """
    grants = pd.DataFrame(result)
    grants = grants[['patentNumber', 'patentApplicationNumber', 'assigneeEntityName', 'filingDate', 'grantDate', 'inventionTitle']]
    grants.to_parquet(os.path.join("patents", f"split_{str(uuid.uuid4())}.parquet"))


async def get_api_resp(session, api):
    """
    Fetch patent data from the API asynchronously.

    Args:
        session (aiohttp.ClientSession): An aiohttp client session.
        api (str): API link to fetch the patents from

    Returns:
        dict: A dictionary containing the fetched patent data.

    Raises:
        aiohttp.ClientResponseError: If the API request encounters an error.

    """
    async with session.get(api) as resp:
        resp.raise_for_status()
        return await resp.json()
    

async def fetch_patent_data(fromDate, toDate, toal_patents):
    """
    Fetch and save patent data pages from the USPTO API.

    Args:
        fromDate (str): The start date for the query.
        toDate (str): The end date for the query.
        toal_patents (int): Total number of patents between dates

    """
    tasks = []

    async with aiohttp.ClientSession() as session:
        # Make a list of all tasks to execute them concurrently
        for start_num in range(0, toal_patents, PAGE_SIZE):
            tasks.append(get_api_resp(session, get_uspto_link(start_num, PAGE_SIZE, fromDate, toDate)))

        # Concurrently execute all the tasks in the tasks list
        for result in await asyncio.gather(*tasks):
            patent_processor(result['results'])


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

    # Create dir to store patent data chunks
    if not os.path.exists("patents"):
        os.makedirs("patents")
    
    # Initialize logging
    logging.basicConfig(filename='patent_fetcher2.log', level=logging.INFO)

    start_time = time.time()
    # First call to get total number of patents between given dates.
    toal_patents = get_total_patent_count(get_uspto_link(0, 1, fromDate, toDate))
    logging.info(f"Total patents between {fromDate} - {toDate} are {toal_patents}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_patent_data(fromDate, toDate, toal_patents))
    loop.close()
    logging.info(f"Total execution time: {(time.time() - start_time)/60.0:.2f} min")
