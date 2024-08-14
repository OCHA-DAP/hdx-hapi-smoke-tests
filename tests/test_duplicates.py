import json
import pytest

from urllib import request

from util.config import BASE_URL, HAPI_APP_IDENTIFIER

from util.requests import fetch_data_from_hapi

from collections import Counter

# ENDPOINT, Full count (2024-08-13), Country filter, Filtered count
ENDPOINT_ROUTER_LIST = [
    ("/api/v1/affected-people/refugees", 580074, "HND", 9140),
    ("/api/v1/affected-people/humanitarian-needs", 279811, "HND", 2589),
    ("/api/v1/coordination-context/operational-presence", 40472, "", None),
    ("/api/v1/coordination-context/funding", 434, "", None),
    ("/api/v1/coordination-context/conflict-event", 1544173, "HTI", 10081),
    ("/api/v1/coordination-context/national-risk", 26, "", None),
    ("/api/v1/food/food-security", 119757, "", None),
    ("/api/v1/food/food-price", 1094401, "HTI", 15948),
    ("/api/v1/population-social/population", 237100, "", None),
    ("/api/v1/population-social/poverty-rate", 630, "", None),
    ("/api/v1/metadata/dataset", 167, "", None),
    ("/api/v1/metadata/resource", 257, "", None),
    ("/api/v1/metadata/location", 250, "", None),
    ("/api/v1/metadata/admin1", 455, "", None),
    ("/api/v1/metadata/admin2", 5458, "", None),
    ("/api/v1/metadata/currency", 128, "", None),
    ("/api/v1/metadata/org", 2531, "", None),
    ("/api/v1/metadata/org-type", 19, "", None),
    ("/api/v1/metadata/sector", 20, "", None),
    ("/api/v1/metadata/wfp-commodity", 1101, "", None),
    ("/api/v1/metadata/wfp-market", 4141, "", None),
]

# BASE_URL = BASE_URL.replace("hapi", "hapi-temporary")
# BASE_URL = "http://localhost:8844/"


def test_fetch_data_from_hapi_with_paging():
    theme = "metadata/admin2"

    query_url = (
        f"{BASE_URL}api/v1/{theme}?"
        f"output_format=csv"
        f"&app_identifier={HAPI_APP_IDENTIFIER}"
    )

    results_1000 = fetch_data_from_hapi(query_url, limit=1000)
    results_10000 = fetch_data_from_hapi(query_url, limit=10000)

    assert results_1000 == results_10000


def test_endpoint_list_against_openapi_definition():
    with request.urlopen(f"{BASE_URL}openapi.json") as openapi_json_url:
        openapi_json = json.load(openapi_json_url)

    openapi_paths = set(list(openapi_json["paths"].keys()))
    openapi_paths.remove("/api/v1/encode_app_identifier")
    openapi_paths.remove("/api/v1/util/version")

    endpoint_paths = {x[0] for x in ENDPOINT_ROUTER_LIST}

    assert endpoint_paths == openapi_paths


@pytest.mark.parametrize(
    "endpoint_router",
    ENDPOINT_ROUTER_LIST,
    ids=[x[0][7:] for x in ENDPOINT_ROUTER_LIST],
)
def test_for_duplicates_all_endpoints_parametrically(endpoint_router):
    theme = endpoint_router[0][1:]
    country = endpoint_router[2]

    query_url = (
        f"{BASE_URL}{theme}?"
        f"output_format=csv"
        f"&location_code={country}"
        f"&app_identifier={HAPI_APP_IDENTIFIER}"
    )

    if "refugees" in query_url:
        query_url = query_url.replace("location_code", "origin_location_code")

    results = fetch_data_from_hapi(query_url, limit=1000)

    results_set = set(results)

    if len(results) != len(list(results_set)):
        counter = Counter(results)
        for k, v in counter.items():
            if v != 1:
                print(k, v, flush=True)
    assert len(results) == len(list(results_set))