from fastapi import FastAPI
from deta import Deta
# from config import config


app = FastAPI()

deta = Deta('c0jrkegd_rQMSFSXNmgb14J4dBL7hGzbrZq2YV12f')

db_users = deta.Base("users")

db_coins = deta.Base("coins")

db_level = deta.Base("levels")

db_links = deta.Base("links")

db_users_stat = deta.Base("users_stat")


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

    db_users_stat.put({
        "First_lvl": False,
        "First_par": "",
        "Second_lvl": False,
        "Second_par": "",
        "Third_lvl": False,
        "Third_par": "",
        "Token": token,
        "is_vtb": False,
        "is_invest": False,
        "is_social": False
    })


@app.post("/insert_coins")
async def insert_coins(n: int, token: str):
    test_fetch = db_coins.fetch({"Token": token})
    key = test_fetch.items[0]["key"]
    update_module = {
        "Coins": test_fetch.items[0]["Coins"] + n
    }
    db_coins.update(update_module, key)


@app.post("/count_levels")
async def count_levels(token: str):
    test_fetch = db_level.fetch({"Token": token})
    key = test_fetch.items[0]["key"]
    update_module = {
        "Level": test_fetch.items[0]["Level"] + 1
    }
    db_level.update(update_module, key)


@app.post("/level_info")
async def level_info(lvl_id: int, par: str, token: str):
    test_fetch = db_users_stat.fetch({"Token": token})
    key = test_fetch.items[0]["key"]
    update_module = {}
    if lvl_id == 1 and not test_fetch.items[0]["First_lvl"]:
        update_module = {
            "First_lvl": True,
            "First_par": par
        }
    elif lvl_id == 2 and not test_fetch.items[0]["Second_lvl"]:
        update_module = {
            "Second_lvl": True,
            "Second_par": par
        }
    elif lvl_id == 3 and not test_fetch.items[0]["Third_lvl"]:
        update_module = {
            "Third_lvl": True,
            "Third_par": par
        }

    db_users_stat.update(update_module, key)


@app.post("/is_vtb")
async def post_vtb_info(token: str):
    test_fetch = db_users_stat.fetch({"Token": token})
    key = test_fetch.items[0]["key"]

    update_module = {}

    if not test_fetch.items[0]["is_vtb"]:
        update_module = {
            "is_vtb": True
        }

    db_users_stat.update(update_module, key)


@app.post("/is_invest")
async def post_invest_info(token: str):
    test_fetch = db_users_stat.fetch({"Token": token})
    key = test_fetch.items[0]["key"]

    update_module = {}

    if not test_fetch.items[0]["is_invest"]:
        update_module = {
            "is_invest": True
        }

    db_users_stat.update(update_module, key)


@app.post("/is_social")
async def post_social_info(token: str):
    test_fetch = db_users_stat.fetch({"Token": token})
    key = test_fetch.items[0]["key"]

    update_module = {}

    if not test_fetch.items[0]["is_social"]:
        update_module = {
            "is_social": True
        }

    db_users_stat.update(update_module, key)


def get_stat(token: str):
    score = 0
    test_fetch = db_users_stat.fetch({"Token": token})
    if test_fetch.items[0]["First_lvl"]:
        score += 1
    if test_fetch.items[0]["Second_lvl"]:
        score += 1
    if test_fetch.items[0]["Third_lvl"]:
        score += 1
    if test_fetch.items[0]["is_invest"]:
        score += 1
    if test_fetch.items[0]["is_social"]:
        score += 1
    if test_fetch.items[0]["is_vtb"]:
        score += 1

    score = score / 6

    return score


@app.get("/stat")
async def get_many_stat():
    score = 0
    res = db_users_stat.fetch()
    all_items = res.items

    # fetch until last is 'None'
    while res.last:
        res = db_users_stat.fetch(last=res.last)
        all_items += res.items

    for row in all_items:
        if row["First_lvl"]:
            score += 1
        if row["Second_lvl"]:
            score += 1
        if row["Third_lvl"]:
            score += 1
        if row["is_invest"]:
            score += 1
        if row["is_social"]:
            score += 1
        if row["is_vtb"]:
            score += 1
        score /= 6
        row["score"] = score
        score = 0

    return all_items
