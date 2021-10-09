from fastapi import FastAPI
from deta import Deta


app = FastAPI()

deta = Deta('c0jrkegd_rQMSFSXNmgb14J4dBL7hGzbrZq2YV12f')

db_users = deta.Base("users")

db_coins = deta.Base("coins")


@app.post("/create_new_user")
async def create_new_user(username: str, token: str, segment: int):
    db_users.put({
        "Username": username,
        "Token": token,
        "Segment": segment
    })


@app.post("/insert_coins")
async def insert_coins(n, token):
    test_fetch = db_coins.fetch({"Token": token})
    key = test_fetch.items[0]["key"]
    update_module = {
        "Coins": test_fetch.items[0]["Coins"] + n
    }
    db_coins.update(update_module, key)
