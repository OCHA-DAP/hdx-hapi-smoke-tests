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
