import motor.motor_asyncio
from functools import cache
from config import load_config

@cache
def get_motor_collection():
    cfg = load_config()
    client = motor.motor_asyncio.AsyncIOMotorClient(cfg["db_config"]["host"], cfg["db_config"]["port"])
    db = client[cfg["db_config"]["database"]]
    return db[cfg["db_config"]["collection"]]