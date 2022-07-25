#! /app/.heroku/node/bin/node

const cb = require("coinbase-pro")
require('dotenv').config()

const key = process.env.API_KEY;
const secret = process.env.API_SECRET;
const passphrase = process.env.PASSPHRASE;
const apiURI = 'https://api.pro.coinbase.com';

let ETHEREUM_SPEND = parseInt(process.env.ETHEREUM_SPEND)

let BITCOIN_SPEND = parseInt(process.env.BITCOIN_SPEND)

const authedClient = new cb.AuthenticatedClient(
  key,
  secret,
  passphrase,
  apiURI
);

const main = async () => {
  if (!Number.isNaN(ETHEREUM_SPEND)) {
    await purchase("ETH-USD", ETHEREUM_SPEND)
  }
  if (!Number.isNaN(BITCOIN_SPEND)) {
    await purchase("BTC-USD", BITCOIN_SPEND)
  }
}

const purchase = async (productTickerString, spentAmountInDollars) => {
  const productInfo = await authedClient.getProductTicker(productTickerString)
  if (productInfo == null || productInfo.price == null || Number.isNaN(productInfo.price)) {
    throw new Error(`bad product info: ${JSON.stringify(productInfo)}`)
  }
  const currentPrice = productInfo.price
  console.log(`product ticker: ${productTickerString}`)
  console.log(`price: ${currentPrice}`)

  const size = parseFloat((spentAmountInDollars / currentPrice).toFixed(4))

  console.log(`size: ${size}`)

  const params = {
    side: 'buy',
    type: 'market',
    size,
    product_id: productTickerString,
  };
  console.log(`date: ${new Date()}`)
  console.log(`params: ${JSON.stringify(params, null, 2)}`)
  const resp = await authedClient.placeOrder(params);
  JSON.stringify(resp, null, 2)
}

main()