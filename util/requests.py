import csv
import json
import requests
import time
from urllib import request

from util.config import HAPI_USER_AGENT


def download_csv(url: str, path: str):
    """
    Download a CSV file from the given URL and save it to the given path
    """
    response = requests.get(url, timeout=50, headers={'User-Agent': HAPI_USER_AGENT})
    with open(path, 'wb') as mapping_file:
        mapping_file.write(response.content)


def read_data_from_csv(csv_file_path):
    """
    Read data from a CSV file and return the header and data rows
    """
    data = []
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            data.append(row)
    return data


def fetch_data_from_hapi(query_url, limit=1000):
    """
    Fetch data from the provided query_url with pagination support.

    Args:
    - query_url (str): The query URL to fetch data from.
    - limit (int): The number of records to fetch per request.

    Returns:
    - list: A list of fetched results.
    """

    headers = {'User-Agent': HAPI_USER_AGENT}

    if 'encode_app_identifier' in query_url:
        with request.urlopen(request.Request(query_url, headers=headers)) as response:
            json_response = json.loads(response.read())

        return json_response

    idx = 0
    results = []

    t0 = time.time()
    while True:
        offset = idx * limit
        url = f'{query_url}&offset={offset}&limit={limit}'
        req = request.Request(url, headers=headers)

        with request.urlopen(req) as response:
            print(f'Getting results {offset} to {offset+limit-1}')
            print(f'{url}', flush=True)
            encoding = response.headers.get_content_charset()

            # print(response.headers, flush=True)
            if 'output_format=json' in query_url:
                json_response = json.loads(response.read())

                results.extend(json_response['data'])
                # If the returned results are less than the limit,
                # it's the last page
                if len(json_response['data']) < limit:
                    break
            else:
                raw = response.read().decode(encoding)
                csv_rows = raw.splitlines()
                # Don't include the header line except for the first file
                if len(results) == 0:
                    results.extend(csv_rows)
                else:
                    results.extend(csv_rows[1:])

                if len(csv_rows) < limit:
                    break
        idx += 1

    print(f'Download took {time.time()-t0:0.2f} seconds', flush=True)
    return results
