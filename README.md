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

The spreadsheet has the following columns, those marked * are used by the smoke test code in this repo:

* location
* Test ID
* Description*
* Args [NOT USED]
* API call*
* \# of results expected
* Expected in each result object [NOT USED]
* Priority
* Implemented?*
* Rules*

To put a carriage return into a cell press `Alt-enter`

For local testing the easiest way to override the target HAPI instance is by editing the default value in this line in `util/config.py` and ensuring `BASE_URL` is not defined as an environment variable:

```python
BASE_URL = os.getenv('BASE_URL', 'https://stage.hapi-humdata-org.ahconu.org/')
```

For local running, if the test spreadsheet has been changed then tests.csv should be deleted and the tests re-discovered.