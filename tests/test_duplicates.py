import pytest
from util.config import BASE_URL, HAPI_APP_IDENTIFIER

from util.requests import fetch_data_from_hapi


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


def test_duplicates_conflict_event_hti_legacy_endpoint():
    theme = "coordination-context/conflict-event"
    country = "HTI"

    query_url = (
        f"{BASE_URL}api/v1/{theme}?"
        f"output_format=csv"
        f"&location_code={country}"
        f"&app_identifier={HAPI_APP_IDENTIFIER}"
    )

    results = fetch_data_from_hapi(query_url, limit=1000)

    results_set = set(results)

    assert len(results) == len(list(results_set))


def test_duplicates_humanitarian_needs_hnd_legacy_endpoint():
    theme = "affected-people/humanitarian-needs"
    country = "HND"

    query_url = (
        f"{BASE_URL}api/v1/{theme}?"
        f"output_format=csv"
        f"&location_code={country}"
        f"&app_identifier={HAPI_APP_IDENTIFIER}"
    )

    results = fetch_data_from_hapi(query_url, limit=1000)

    results_set = set(results)

    assert len(results) == len(list(results_set))


@pytest.mark.xfail
def test_duplicates_conflict_event_hti_new_endpoint():
    theme = "coordination-context/conflict-event"
    country = "HTI"

    base_url = BASE_URL.replace("hapi", "hapi-temporary")
    query_url = (
        f"{base_url}api/v1/{theme}?"
        f"output_format=csv"
        f"&location_code={country}"
        f"&app_identifier={HAPI_APP_IDENTIFIER}"
    )

    results = fetch_data_from_hapi(query_url, limit=1000)

    results_set = set(results)

    assert len(results) == len(list(results_set))


@pytest.mark.xfail
def test_duplicates_humanitarian_needs_hnd_new_endpoint():
    theme = "affected-people/humanitarian-needs"
    country = "HND"

    base_url = BASE_URL.replace("hapi", "hapi-temporary")

    query_url = (
        f"{base_url}api/v1/{theme}?"
        f"output_format=csv"
        f"&location_code={country}"
        f"&app_identifier={HAPI_APP_IDENTIFIER}"
    )

    results = fetch_data_from_hapi(query_url, limit=1000)

    results_set = set(results)

    assert len(results) == len(list(results_set))
