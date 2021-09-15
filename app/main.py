import ccxt
import pandas as pd
import os
from dotenv import load_dotenv
import redis
from datetime import timedelta
from fastapi import FastAPI
import json
import sys


def redis_connect() -> redis.client.Redis:
    try:
        client_ = redis.Redis(host='redis', port=6379, db=0)
        ping = client_.ping()
        if ping is True:
            return client_
    except redis.AuthenticationError:
        print('Authentication Error with Redis')
        sys.exit(1)


client = redis_connect()


def get_balances_from_api() -> dict:
    load_dotenv()
    exchange = ccxt.kucoin({
        'apiKey': os.getenv('API_KEY'),
        'secret': os.getenv('SECRET'),
        'password': os.getenv('PASSWORD')
    })
    balances_ = exchange.fetch_balance()
    columns_ = ['id', 'currency', 'account_type', 'balance', 'available', 'holds']
    data_ = []
    for data in balances_['info']['data']:
        data_.append([
            data['id'], data['currency'], data['type'],
            data['balance'], data['available'], data['holds']
        ])
    df_ = pd.DataFrame(data=data_, columns=columns_)
    df_.set_index('id', drop=True, inplace=True)
    return df_.to_dict()


def get_balances_from_cache() -> str:
    balances_ = client.get('balances')
    return balances_


def set_balances_to_cache(balances_: str) -> bool:
    state = client.setex('balances', timedelta(seconds=30), value=balances_)
    return state


def balances_req() -> dict:
    data = get_balances_from_cache()

    if data is not None:
        data = json.loads(data)
        data['cache'] = True
        return data
    else:
        data = get_balances_from_api()
        data['cache'] = False
        data = json.dumps(data)
        state = set_balances_to_cache(data)

        if state is True:
            return json.loads(data)


app = FastAPI()


@app.get('/')
def view():
    return balances_req()
