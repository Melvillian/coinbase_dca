# Dollar Cost Averaging Bot

A simple DCA (dollar cost averaging) bot that uses the
[Coinbase Python SDK](https://docs.cdp.coinbase.com/advanced-trade/docs/sdk-overview)
to executes a sell of a product (e.g. `"BTC-USD"`) for some amount of USD (e.g.
`$500`). It is expected that you will run this in some sort of cron job so that
it runs every day (or whatever interval you want).

## Getting Started

### Creating Secure Coinbase API Key

Create an account on Coinbase and create an API key and secret, [which you can do here](https://portal.cdp.coinbase.com/access/api). Make sure you generate a "Trading Key", not a "General Key", because Trading Keys are the new authentication system that Coinbase uses.

You will need to provide an IP address (or IP address range) from which this script is allowed to execute. You have two options, 1 much easier but less secure, and 2 secure but much harder:

1. Use an IP whitelist of `0.0.0.0/0`, which will allow any IP address to access the API. Obviously if your API key is discovered by attackers (because you commit it to a public repo, or your local machine is compromised) you could have all of your coin sold for some shitcoin. So beware of this option.
   
2. Setup a VPN with a static IP and run your script from there. I don't do this because it's complicated and I secure my local machine well enough

### Setup Envvars

Run `cp .env.example .env` and set all variables to your desired values.

### Install Poetry

If you don't have Poetry installed, [you can do that here](https://python-poetry.org/docs/#installation). Then, run `poetry install`

### Execute the Trade

`poetry run main`

This will execute the buy or sell for the specified dollar amount, based on your .env variables.

## Building A Single Binary Executable, Suitable For A Cron Job

On its own this script cannot implement DCA, because to correctly do DCA you need to sell/buy at a fixed interval (such as once a day) over a long time period. In order to make that as easy as possible, we can build a single binary executable that can be run directly by a cron job (or Mac's equivalent, launchd).

### Build Steps

1. Install [pyinstaller](https://pyinstaller.org/en/stable/installation.html) with `pip install pyinstaller`

2. From the project root, run `pyinstaller --add-data=".env:." --onefile coinbase_dca/main.py`. This will create a single executable at `dist/main`, which you can run from anywhere using `/path/to/dist/main`.

3. Finally, execute your buy/sell periodically using either

   - [cron](https://phoenixnap.com/kb/set-up-cron-job-linux) if on Linux
   - [launchd](https://alvinalexander.com/mac-os-x/mac-osx-startup-crontab-launchd-jobs/) if you're using a Mac
      
      - tl;dr: make a plist file, and then run `launchctl load /path/to/file.plist`
   - 🤷 if you're on Windows
