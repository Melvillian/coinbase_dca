from coinbase.rest import RESTClient
from dotenv import load_dotenv
import os
from json import dumps
from datetime import datetime


load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
product_id_env = os.getenv("PRODUCT_ID")
amount_to_sell_in_usd_env = os.getenv("AMOUNT_TO_SELL_IN_USD")


def dollar_cost_averaging_sell(client, product_id, amount_to_sell_in_usd):
    # get best bid for product (e.g. "BTC-USD")
    bid_ask_spread = client.get_best_bid_ask(product_id)
    best_bid = float(bid_ask_spread["pricebooks"][0]["bids"][0]["price"])

    # calculate the amount of the base currency (e.g. BTC) to sell for the given
    # amount to sell (measured in e.g. USD)
    amount_to_sell_in_base_currency = f"{(amount_to_sell_in_usd / best_bid):.5f}"

    # use the current day as the client_order_id, which will ensure
    # we only make 1 market order per day as long as the
    # client_order_id's follow this format
    client_order_id = datetime.now().strftime("%Y-%m-%d")

    # make the sell order. If we've already tried to make an order
    # at for this day, it will fail. This adds a simple defense against
    # the script making multiple orders and selling too much
    resp = client.market_order_sell(
        client_order_id, product_id, amount_to_sell_in_base_currency
    )

    print(dumps(resp, indent=2))


def main():
    client = RESTClient(api_key=api_key, api_secret=api_secret)

    # sell $500's worth of BTC
    dollar_cost_averaging_sell(client, product_id_env, amount_to_sell_in_usd_env)
