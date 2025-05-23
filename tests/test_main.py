import os
from io import StringIO
import requests
import pytest
import csv
from util.config import (
    BASE_URL,
    TESTS_SPREADSHEET_URL,
    HEADER_API_CALL,
    HEADER_RULES,
    HEADER_DESCRIPTION,
    HEADER_ENABLED,
    HAPI_APP_IDENTIFIER,
)

from util.requests import download_csv, read_data_from_csv
from util.rules import parse_rules


DOWNLOAD_PATH = 'tests.csv'

# if os.path.exists(DOWNLOAD_PATH):
#     os.remove(DOWNLOAD_PATH)

download_csv(TESTS_SPREADSHEET_URL, DOWNLOAD_PATH)
data_all_columns = read_data_from_csv(DOWNLOAD_PATH)
data = [[row[HEADER_DESCRIPTION], row] for row in data_all_columns if row[HEADER_ENABLED] == 'TRUE']


@pytest.mark.parametrize('description, test_info', data)
def test_json_rest_api(description, test_info):
    rules = parse_rules(test_info[HEADER_RULES])

    relative_url = (
        test_info[HEADER_API_CALL][1:] if test_info[HEADER_API_CALL].startswith('/') else test_info[HEADER_API_CALL]
    )

    if '?' in relative_url:
        relative_url += f'&app_identifier={HAPI_APP_IDENTIFIER}'
    else:
        relative_url += f'?app_identifier={HAPI_APP_IDENTIFIER}'
    endpoint_url = f'{BASE_URL}{relative_url}'

    response = requests.get(endpoint_url)
    response_dict = response.json()
    object_list = response_dict.get('data', [])

    assert response.status_code == 200, ', url:' + endpoint_url

    for rule in rules:
        output_description = (
            f'\nDescription: {rule.description}\nActual value: '
            f'{str(rule.input_list_builder(object_list))}\nURL: {endpoint_url}'
        )
        assert rule.operator(rule.input_list_builder(object_list), rule.value), output_description
        # for debug
        # result = rule.operator(rule.input_list_builder(object_list), rule.value)
        # if result:
        #     assert True
        # else:
        #     assert True


def test_csv_rest_api():
    endpoint_url = f'{BASE_URL}api/v1/metadata/dataset?output_format=csv&app_identifier={HAPI_APP_IDENTIFIER}'
    print(endpoint_url, flush=True)
    response = requests.get(endpoint_url)

    assert response.status_code == 200

    csv_data = response.text

    # Parse the CSV data into a list of rows
    csv_reader = csv.DictReader(StringIO(csv_data))
    csv_rows = list(csv_reader)

    assert len(csv_rows) > 2
