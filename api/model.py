from os import environ as env

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .app import app

uri = f'mongodb+srv://{env.get("mongo_atlas_username")}:{env.get("mongo_atlas_passwd")}@cluster0.th5fhnb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))


def select_keys(raw_obj, keys):
    """Create a DAO"""
    if type(raw_obj) is not dict:
        return {}
    return {key: raw_obj[key] for key in keys}


def make_user_dao(user_raw):
    """make a user DAO"""
    keys = ["username"]
    return select_keys(user_raw, keys)


def ping():
    """Return True if the database is available"""
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        print(e)
        return False


def get_user(username):
    """Returns specified user"""
    db = client.Cluster0
    user = db.users.find_one({"username": username})
    user = make_user_dao(user)
    return user


def get_or_create_user(username):
    """Create a new user with the specified username"""
    if user := get_user(username): # Remember that an empty dict is falsy
        return user
    else:
        return create_user(username)


def create_user(username):
    """Create a new user with the specified username"""
    db = client.Cluster0
    new_obj = {"username": username}
    record_id = db.users.insert_one(new_obj)
    return make_user_dao(new_obj)
