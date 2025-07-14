import requests
import pandas as pd
import time
from streamlit import cache_data

@cache_data(ttl=600)
def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "price_change_percentage": "1h,24h,7d"
    }
    response = requests.get(url, params=params)
    return pd.DataFrame(response.json())

@cache_data(ttl=600)
def get_price_history(coin_id, days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}

    for _ in range(3):
        response = requests.get(url, params=params)
        if response.status_code == 429:
            time.sleep(5)
        else:
            break

    if response.status_code != 200:
        raise Exception(f"Failed to fetch prices: {response.status_code}")

    return [point[1] for point in response.json()["prices"]]

@cache_data(ttl=600)
def get_price_history_timestamps(coin_id, days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}

    retries = 5
    delay = 2  # Start with 2 seconds

    for attempt in range(retries):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if "prices" not in data:
                raise ValueError(f"No 'prices' key found in response for {coin_id}")
            return [point[0] for point in data["prices"]]

        elif response.status_code == 429:
            wait = delay * (2 ** attempt)
            print(f"[WARN] Rate limited for {coin_id}. Retrying in {wait}s...")
            time.sleep(wait)
        else:
            raise Exception(f"Unexpected error {response.status_code} for {coin_id}")

    raise Exception(f"Failed to fetch timestamps for {coin_id} after {retries} retries.")