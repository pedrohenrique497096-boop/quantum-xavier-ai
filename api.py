from fastapi import FastAPI
from database.trades import get_signals
from data.market import get_price,get_candles

app=FastAPI()

@app.get("/signals")

def signals():

    return get_signals()


@app.get("/price/{symbol}")

def price(symbol):

    return {
        "symbol":symbol,
        "price":get_price(symbol)
    }


@app.get("/chart/{symbol}")

def chart(symbol):

    return get_candles(symbol)
