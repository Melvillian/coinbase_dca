# Dollar Cost Averaging Bot

A simple DCA (dollar cost averaging) bot that uses the
[Coinbase Python SDK](https://docs.cloud.coinbase.com/advanced-trade-api/docs/sdk-overview)
to executes a sell of a product (e.g. `"BTC-USD"`) for some amount of USD (e.g.
`$500`). It is expected that you will run this in some sort of cron job so that
it runs every day (or whatever interval you want).

## Getting Started

1. Create an account on Coinbase and create an API key and secret,
   [which you can do here](https://cloud.coinbase.com/access/api). Make sure you
   generate a "Trading Key", not a "General Key", because Trading Keys are the
   new authentication system that Coinbase uses. Also note that you will need to
   provide an IP address (or IP address range) from which this script is allowed
   to execute. I have used [WhatsMyIp](https://whatismyipaddress.com/) to get my
   local IP address, but I'm aware that my ISP may change that IP address at any
   time. c'est la vie.

2. Once you have the `API_KEY` and `API_SECRET`, run `cp .env.example .env` and
   fill in your API key + secret info. Note, currently the bot only sells, there
   is a TODO to add the ability to buy as well.

3. If you don't have Poetry installed,
   [you can do that here](https://python-poetry.org/docs/#installation). Then,
   run `poetry install`

4. Open up `coinbase_dca/main.py` and go to the `def main():` line. Update the
   product id (e.g. `"BTC-USD"`) as well as the dollar amounts to match what you
   want to trade. You can make multiple calls to `dollar_cost_averaging_sell`
   depending on how many different product ids you want to sell/buy

5. Finally, execute the bot with `poetry run main`. Currently this will sell
   $500 worth of both `"ETH-USD"` and `"BTC-USD"`

## Building A Single Binary Executable, Suitable For A Cron Job

On its own this script cannot implement DCA, because to correctly do DCA you
need to sell/buy at a fixed interval (such as once a day) over a long time
period. In order to make that as easy as possible, we can build a single binary
executable that can be run directly by a cron job.

### Steps

1. Install [pyinstaller](https://pyinstaller.org/en/stable/installation.html)

2. From the project root, run `pyinstaller --add-data=".env:." --onefile coinbase_dca/main.py`. This will create a single executable at `dist/main`, which you can run from anywhere using `/path/to/dist/main`.

3. Finally, create a cron job (using either
   [cron](https://phoenixnap.com/kb/set-up-cron-job-linux) or
   [launchd](https://alvinalexander.com/mac-os-x/mac-osx-startup-crontab-launchd-jobs/)
   if you're using a Mac) and point it at the binary you created in step 2.

## TODO

- [X] Add the ability to buy crypto with a function called
      `dollar_cost_averaging_buy`
- [X] Figure out how to make an easy build process that included the env vars in the final binary
