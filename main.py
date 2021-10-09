from fastapi import FastAPI
from deta import Deta
# from config import config


app = FastAPI()

deta = Deta('c0jrkegd_rQMSFSXNmgb14J4dBL7hGzbrZq2YV12f')

db_users = deta.Base("users")

db_coins = deta.Base("coins")

db_level = deta.Base("levels")

db_links = deta.Base("links")




@app.post("/create_new_user")
async def create_new_user(username: str, token: str, segment: int):
    db_users.put({
        "Username": username,
        "Token": token,
        "Segment": segment
    })

    db_coins.put({
        "Coins": 0,
        "Token": token
    })

    db_level.put({
        "levels": 0,
        "Token": token
    })

    db_coins.put({
        "Token": token,
        "link": False
    })


@app.post("/insert_coins")
async def insert_coins(n: int, token: str):
    test_fetch = db_coins.fetch({"Token": token})
    key = test_fetch.items[0]["key"]
    update_module = {
        "Coins": test_fetch.items[0]["Coins"] + n
    }
    db_coins.update(update_module, key)


@app.post("/levels")
async def levels(token: str):
    test_fetch = db_coins.fetch({"Token": token})
    key = test_fetch.items[0]["key"]
    update_module = {
        "levels": test_fetch.items[0]["Coins"] + 1
    }




