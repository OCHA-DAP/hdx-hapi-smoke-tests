import json
import pytest

from urllib import request

from util.config import BASE_URL, HAPI_APP_IDENTIFIER

from util.requests import fetch_data_from_hapi

from collections import Counter

# ENDPOINT, Country filter, Full count (2024-08-13), Filtered count
ENDPOINT_ROUTER_LIST = [
    ('/api/v2/affected-people/refugees-persons-of-concern', 'HND'),  # , 580074, 9140
    ('/api/v2/affected-people/humanitarian-needs', 'HND'),  # 279811, 2589
    ('/api/v2/affected-people/idps', ''),
    ('/api/v2/affected-people/returnees', ''),
    ('/api/v2/coordination-context/operational-presence', ''),  # 40472,
    ('/api/v2/coordination-context/funding', ''),  # 434
    ('/api/v2/coordination-context/conflict-events', 'HTI'),  # 1544173, 10081
    ('/api/v2/coordination-context/national-risk', ''),  # 26,
    ('/api/v2/food-security-nutrition-poverty/food-security', ''),  # 119757,
    ('/api/v2/food-security-nutrition-poverty/food-prices-market-monitor', 'HTI'),  # 1094401, 15948
    ('/api/v2/geography-infrastructure/baseline-population', ''),  # 237100,
    ('/api/v2/food-security-nutrition-poverty/poverty-rate', ''),  # 630,
    ('/api/v2/metadata/dataset', ''),  # 167,
    ('/api/v2/metadata/resource', ''),  # 257,
    ('/api/v2/metadata/location', ''),  # 250,
    ('/api/v2/metadata/admin1', ''),  # 455,
    ('/api/v2/metadata/admin2', ''),  # 5458,
    ('/api/v2/metadata/currency', ''),  # 128,
    ('/api/v2/metadata/org', ''),  # 2531,
    ('/api/v2/metadata/org-type', ''),  # 19,
    ('/api/v2/metadata/sector', ''),  # 20,
    ('/api/v2/metadata/wfp-commodity', ''),  # 1101,
    ('/api/v2/metadata/wfp-market', ''),  # 4141,
    ('/api/v2/metadata/data-availability', ''),
    ('/api/v2/climate/rainfall', ''),
]


def test_fetch_data_from_hapi_with_paging():
    theme = 'metadata/admin2'

    query_url = f'{BASE_URL}api/v2/{theme}?output_format=csv&app_identifier={HAPI_APP_IDENTIFIER}'

    results_1000 = fetch_data_from_hapi(query_url, limit=1000)
    results_10000 = fetch_data_from_hapi(query_url, limit=10000)

    assert len(results_1000) != 0
    assert len(results_10000) != 0
    assert results_1000 == results_10000


def test_endpoint_list_against_openapi_definition():
    print(f'{BASE_URL}openapi.json', flush=True)
    with request.urlopen(f'{BASE_URL}openapi.json') as openapi_json_url:
        openapi_json = json.load(openapi_json_url)

    openapi_paths = set(list(openapi_json['paths'].keys()))
    openapi_paths.remove('/api/v2/encode_app_identifier')
    openapi_paths.remove('/api/v2/util/version')

    endpoint_paths = {x[0] for x in ENDPOINT_ROUTER_LIST}

    assert endpoint_paths == openapi_paths


@pytest.mark.parametrize(
    'endpoint_router, country',
    ENDPOINT_ROUTER_LIST,
    ids=[
        x[0][7:]
        for x in ENDPOINT_ROUTER_LIST  # Makes the labels for the parameterized tests
    ],
)
def test_for_duplicates_all_endpoints_parametrically(endpoint_router, country):
    if BASE_URL.endswith('/'):
        theme = endpoint_router[0][1:]
    else:
        theme = endpoint_router[0]

    query_url = (
        f'{BASE_URL}{theme}?' f'output_format=csv' f'&location_code={country}&app_identifier={HAPI_APP_IDENTIFIER}'
    )

    if 'refugees' in query_url:
        query_url = query_url.replace('location_code', 'origin_location_code')

    results = fetch_data_from_hapi(query_url, limit=1000)

    results_set = set(results)

    if len(results) != len(list(results_set)):
        counter = Counter(results)
        for k, v in counter.items():
            if v != 1:
                print(k, v, flush=True)
    assert len(results) == len(list(results_set))
