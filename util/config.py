import os


BASE_URL = os.getenv("BASE_URL", "https://HAPI_SERVER_URL/")
HAPI_APP_IDENTIFIER = os.getenv("HAPI_APP_IDENTIFIER", "")
TESTS_SPREADSHEET_URL = os.getenv('TESTS_SPREADSHEET_URL',
                                  'https://docs.google.com/spreadsheets/d/e/2PACX-1vSfC6zhjjg1MmwoBV2swtKt3mIseFLkzwHgsdJkt6E7wyGW0JdgoV_sbQhlk1CFp8BIt4cJ5-_lKKn9/pub?gid=1213905081&single=true&output=csv')

HEADER_API_CALL = 'API call'
HEADER_RULES = 'Rules'
HEADER_DESCRIPTION = 'Description'
HEADER_ENABLED = 'Implemented?'
