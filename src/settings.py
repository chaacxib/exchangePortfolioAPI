import os
from dotenv import load_dotenv

load_dotenv()

# YAHOO FINANCE SETTINGS
YH_FINANCE_API_HOST = 'yh-finance.p.rapidapi.com'
YH_FINANCE_API_KEY = os.getenv(key='YH_FINANCE_API_KEY')

YH_FINANCE_API_SUMMARY_URL = f'https://{YH_FINANCE_API_HOST}/stock/v2/get-summary'

YH_FINANCE_API_HEADERS = {
    'x-rapidapi-host': YH_FINANCE_API_HOST,
    'x-rapidapi-key': YH_FINANCE_API_KEY
}

# DEVELOPMENT SETTINGS
ON_CLOUD = bool(os.getenv(key='ON_CLOUD', default=False))
STAGE_PREFIX = os.getenv(key='STAGE_PREFIX', default='')
LOCAL_DATABASE_HOST = os.getenv(key='LOCAL_DATABASE_HOST', default="http://localhost:4567")

# FASTAPI SETTINGS
API_VERSION = '1.0.0'
API_TITLE = 'Exchange Portfolio API'
API_DESCRIPTION = 'Simple API for custom investing portfolio watch list'
