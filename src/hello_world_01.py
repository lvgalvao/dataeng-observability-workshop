import logfire
import requests

logfire.configure()
logfire.instrument_requests()

requests.get("https://httpbin.org/get")

logfire.info('Hello, {name}!', name='world')