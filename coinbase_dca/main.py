from coinbase.rest import RESTClient
from dotenv import load_dotenv
import os
from json import dumps
from datetime import datetime


load_dotenv()
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

    # buy the coin
    dollar_cost_averaging_buy(client, "BTC-USD", 100)
    dollar_cost_averaging_buy(client, "ETH-USD", 300)


if __name__ == "__main__":
    main()
