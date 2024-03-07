from .lib.replace_me import get, post, patch

from coinbase.rest import RESTClient
from dotenv import load_dotenv
import os
from json import dumps

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


def main():
    client = RESTClient(api_key=api_key, api_secret=api_secret)

    accounts = client.get_accounts()

    nonzero_accounts = []

    print(dumps(accounts, indent=2))
