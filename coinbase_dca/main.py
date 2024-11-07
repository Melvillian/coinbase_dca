from coinbase.rest import RESTClient
from dotenv import load_dotenv
import os
import sys
from json import dumps
from datetime import datetime


# This opaque looking function handles the vagaries of how Pyinstaller deals with bundling the .env
# file when it creats a --onefile single binary executable.
# To understand more you can read:
# https://gist.github.com/Shrestha7/ecc6cf8b4506ca3901a0542ad82c1cda
# https://github.com/theskumar/python-dotenv/issues/259
def handle_bundled_load_dotenv():
    # Determine if the application is running in a bundled executable
    if getattr(sys, "frozen", False):
        # If it's running as a bundled executable, use this path
        application_path = sys._MEIPASS
    else:
        # If it's running as a normal Python script, use this path
        application_path = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the .env file
    dotenv_path = os.path.join(application_path, ".env")

    load_dotenv(dotenv_path)


handle_bundled_load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


def dollar_cost_averaging_sell(client, product_id, amount_to_sell_in_usd):
    """Sell a given USD amount of a product (e.g. BTC-USD) at market price"""
    assert amount_to_sell_in_usd < 10_000  # limit the damage that can be done
    amount_to_sell_in_usd = str(amount_to_sell_in_usd)

    # To make the unique client_order_id, we use the combination of product id
    # (e.g. "BTC-USD") concatenated with the  current day, which will
    # ensure we only make 1 market order per day per product_id as long as the
    # client_order_id's follow this format
    client_order_id = f"{product_id}-{datetime.now().strftime('%Y-%m-%d')}"

    # for sells we need to use supply the amount of the first asset
    # in the product id (e.g. "BTC" in "BTC-USD") as the "base_size".
    # This is different from `dollar_cost_averaging_buy` where we need to
    # supply the amount of the second asset in the product id (e.g. "USD" in "BTC-USD")
    # as the "quote_size"

    # use the coinbase python sdk to fetch the current price of BTC in USD
    resp = client.get_product_ticker(product_id)
    price_of_btc_in_usd = float(resp["price"])
    amount_to_sell_in_btc = float(amount_to_sell_in_usd) / price_of_btc_in_usd
    amount_to_sell_in_btc = str(amount_to_sell_in_btc)

    # make the sell order. If we've already tried to make an order
    # for this product_id and day, it will simply return the existing
    # order information. This adds a simple defense against the script
    # making multiple orders and selling too much
    resp = client.market_order_sell(
        client_order_id=client_order_id,
        product_id=product_id,
        quote_size=amount_to_sell_in_usd,
    )

    # log the current time and order data so we can debug if needed
    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    print(dumps(resp, indent=2))


def dollar_cost_averaging_buy(client, product_id, amount_to_buy_in_usd):
    """Buy a given USD amount of a product (e.g. BTC-USD) at market price"""
    assert amount_to_buy_in_usd < 10_000  # limit the damage that can be done
    amount_to_buy_in_usd = str(amount_to_buy_in_usd)

    # To make the unique client_order_id, we use the combination of product id
    # (e.g. "BTC-USD") concatenated with the current day, which will
    # ensure we only make 1 market order per day per product_id as long as the
    # client_order_id's follow this format
    client_order_id = f"{product_id}-{datetime.now().strftime('%Y-%m-%d')}"

    # make the buy order. If we've already tried to make an order
    # for this product_id and day, it will simply return the existing
    # order information. This adds a simple defense against the script
    # making multiple orders and buying too much
    resp = client.market_order_buy(
        client_order_id=client_order_id,
        product_id=product_id,
        quote_size=amount_to_buy_in_usd,
    )

    # log the current time and order data so we can debug if needed
    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    print(dumps(resp, indent=2))


def main():
    client = RESTClient(api_key=api_key, api_secret=api_secret)

    # sell the coin
    dollar_cost_averaging_sell(client, "BTC-USD", 2000)


if __name__ == "__main__":
    main()
