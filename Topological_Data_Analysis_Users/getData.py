import requests
import pandas as pd
import os
from dotenv import load_dotenv


def get_data():
    load_dotenv()
    ADDRESS_TO_INSPECT = (
        "0x54522da62a15225c95b01bd61ff58b866c50471f"  # Primitive Manager Address
    )
    r = requests.get(
        "https://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&sort=asc&apikey={}".format(
            ADDRESS_TO_INSPECT, os.environ["ETHERSCAN_API"]
        )
    )
    a = r.json()
    df = pd.DataFrame(a["result"])
    users = df["from"]
    return users


def get_users_nieghbors(user):
    # for user in users:
    r = requests.get(
        "https://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&page=1&sort=asc&apikey={}".format(
            user, os.environ["ETHERSCAN_API"]
        )
    )
    df = pd.DataFrame(r.json()["result"])
    df = df["to"].drop_duplicates()
    return df
