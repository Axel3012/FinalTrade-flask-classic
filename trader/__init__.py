from flask import Flask 

APIKEY = '2F4FC920-40BD-45B4-B8EB-F324067D3CAB'

MONEDAS = [("EUR" , "Euro"),
           ("BTC" , "Bitcoin"),
           ("ETH" , "Ethereum"),
           ("BNB" , "Binance Coin"),
           ("BCH" , "Bitcoin Cash"),
           ("LUNA" , "Luna Coin"),
           ("SOL" , "SOL"),
           ("LINK" , "ChainLink"),
           ("ATOM" , "Cosmos"),
           ("USDT" , "Tether"),
           ("DOGE" , "DogeCoin")
           ]


app = Flask(__name__)
app.config.from_prefixed_env()
