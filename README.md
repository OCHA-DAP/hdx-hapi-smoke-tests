# hdx-hapi-smoke-tests

## Contributions

For developers the code should be cloned installed from the [GitHub repo](https://github.com/OCHA-DAP/hdx-hapi-smoke-tests), and a virtual enviroment created:

```shell
python -m venv venv
source venv/Scripts/activate
```

And then an editable installation created:

```shell
pip install -r requirements.txt
```

To run locally the environment variables `BASE URL` and `HAPI_APP_IDENTIFIER` need to be set, the majority of the test suite is generated from a csv file stored as a Google Sheet whose URL is included in the repo but can be overridden with the environment `TEST_SPREADSHEET_URL`.
