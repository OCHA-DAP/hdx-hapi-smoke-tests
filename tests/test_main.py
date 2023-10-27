from io import StringIO
import requests
import pytest
import csv
from util.config import BASE_URL, TESTS_SPREADSHEET_URL, HEADER_API_CALL, HEADER_RULES, HEADER_DESCRIPTION, HEADER_ENABLED

from util.requests import download_csv, read_data_from_csv
from util.rules import parse_rules


download_csv(TESTS_SPREADSHEET_URL, "tests.csv")
data_all_columns = read_data_from_csv("tests.csv")
data = [[row[HEADER_DESCRIPTION], row] for row in data_all_columns if row[HEADER_ENABLED] == 'TRUE']


@pytest.mark.parametrize("description, test_info", data)
def test_json_rest_api(description, test_info):
    
    rules = parse_rules(test_info[HEADER_RULES])

    relative_url = test_info[HEADER_API_CALL][1:] if test_info[HEADER_API_CALL].startswith('/') else test_info[HEADER_API_CALL]
    endpoint_url = f'{BASE_URL}{relative_url}'
    response = requests.get(endpoint_url)
    object_list = response.json()

    assert response.status_code == 200

    for rule in rules:
        assert rule.operator(rule.input_list_builder(object_list), rule.value), rule.description

def test_csv_rest_api():
    endpoint_url = f'{BASE_URL}api/admin1?output_format=csv'
    response = requests.get(endpoint_url)

    assert response.status_code == 200
    
    csv_data = response.text

    # Parse the CSV data into a list of rows
    csv_reader = csv.DictReader(StringIO(csv_data))
    csv_rows = list(csv_reader)

    assert len(csv_rows) > 25