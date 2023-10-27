import os


BASE_URL = os.getenv("BASE_URL", "https://stage.hapi-humdata-org.ahconu.org/")
TESTS_SPREADSHEET_URL = os.getenv('TESTS_SPREADSHEET_URL',
                                  'https://docs.google.com/spreadsheets/d/e/2PACX-1vTFjBRwN0KGAhxH1ujSQR17fjaSabkHCht3Jhq9gUqjON5ONYx_K_avBui4SulTgZ3SrKkFBoFRHZIH/pub?gid=0&single=true&output=csv')

HEADER_API_CALL = 'API call'
HEADER_RULES = 'Rules'
HEADER_DESCRIPTION = 'Description'
HEADER_ENABLED = 'Implemented?'
