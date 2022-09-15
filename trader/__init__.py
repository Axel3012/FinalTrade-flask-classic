from flask import Flask 

RUTA = 'data/trade.db'

APIKEY = '2F4FC920-40BD-45B4-B8EB-F324067D3CAB'

MONEDAS = [("EUR" , "Euro"),
           ("BTC" , "Bitcoin"),
           ("ETH" , "Ethereum"),
           ("DOGE" , "DogeCoin")
           ]

app = Flask(__name__)
app.config.from_prefixed_env()
