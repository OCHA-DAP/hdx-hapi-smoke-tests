import os


BASE_URL = os.getenv("BASE_URL", "https://HAPI_SERVER_URL/")
TESTS_SPREADSHEET_URL = os.getenv('TESTS_SPREADSHEET_URL',
                                  'https://docs.google.com/spreadsheets/d/e/2PACX-1vQsBPljVPAc88mS7ubhMvbYFArcRXQDtYVajfpq2UIGFbRx6ZzGC3VNLNt_HLzQ9idqGW1XuGaxwP4H/pub?gid=0&single=true&output=csv')

HEADER_API_CALL = 'API call'
HEADER_RULES = 'Rules'
HEADER_DESCRIPTION = 'Description'
HEADER_ENABLED = 'Implemented?'
