import os


# YAHOO FINANCE SETTINGS
YH_FINANCE_API_HOST = 'yh-finance.p.rapidapi.com'
YH_FINANCE_API_KEY = os.getenv(key='ON_CLOUD')

YH_FINANCE_API_SUMMARY_URL = f'https://{YH_FINANCE_API_HOST}/stock/v2/get-summary'

YH_FINANCE_API_HEADERS = {
    'x-rapidapi-host': YH_FINANCE_API_HOST,
    'x-rapidapi-key': YH_FINANCE_API_KEY
}

# DEVELOPMENT SETTINGS
ON_CLOUD = bool(os.getenv(key='ON_CLOUD', default=False))
