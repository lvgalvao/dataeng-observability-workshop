import logfire
import requests

logfire.configure()
logfire.instrument_requests()

URL='https://api.coinbase.com/v2/prices/spot?currency=USD#'

def pipeline():
    response = requests.get(url=URL)
    data_dict = response.json()
    logfire.info(f'Bitcoin value, {data_dict}!')
    

pipeline()