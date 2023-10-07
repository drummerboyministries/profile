from os import environ as env

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .app import app

uri = f'mongodb+srv://{env.get("mongo_atlas_username")}:{env.get("mongo_atlas_passwd")}@cluster0.th5fhnb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))


class ForbiddenError(Exception):
    def __init__(self, message="You are not allowed to do that"):
        self.message = message
        super().__init__(self.message)


def select_keys(raw_obj, keys):
    """Create a DAO"""
    if type(raw_obj) is not dict:
        return {}
    return {key: raw_obj.get(key, None) for key in keys}


def make_profile_dao(user_raw):
    """make a user profile DAO out of the user"""
    keys = ["username", "profile_pic", "background_pic", "bio", "nonexistent_field"]
    return select_keys(user_raw, keys)


def make_user_dao(user_raw):
    """make a user user DAO out of the user"""
    keys = ["username", "auth0_sub", "profile_pic", "background_pic", "bio"]
    return select_keys(user_raw, keys)


def ping():
    """Return True if the database is available"""
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        print(e)
        return False


def get_profile(username="", auth0_subject=""):
    """Returns specified user"""
    user = get_user(username, auth0_subject)
    if not user:
        return None
    return make_profile_dao(user)


def get_user(username="", auth0_subject=""):
    db = client.Cluster0
    if username and auth0_subject:
        raise ValueError("Cannot specify both username and auth0_subject")
    if username:
        user = db.users.find_one({"username": username})
    elif auth0_subject:
        user = db.users.find_one({"auth0_sub": auth0_subject})
    else:
        raise ValueError("Must specify either username or auth0_subject")
    return make_user_dao(user)


def get_or_create_user(username):
    """Create a new user with the specified username"""
    if user := get_user(username): # Remember that an empty dict is falsy
        return user
    else:
        return create_user(username)


def create_user(user_obj_or_name, fields={}):
    """Create a new user with the specified username or document structure"""
    db = client.Cluster0
    if type(user_obj_or_name) is not str:
        assert type(user_obj_or_name) is dict, "Username must be a string or dict"
        new_obj = user_obj_or_name
    else:
        new_obj = {"username": user_obj_or_name}

    new_obj.update(fields)
    if existing_user := get_user(new_obj["username"]):
        return add_fields(existing_user, new_obj)
    record_id = db.users.insert_one(new_obj)
    return make_user_dao(new_obj)


def add_fields(username, add_dict={}):
    """Add a new fields to the user"""
    db = client.Cluster0
    user = get_user(username=username)
    if add_dict.get("auth0_sub", "") and user.get("auth0_sub", ""):
        raise ForbiddenError("Cannot claim profile")
    
    if not user:
        user = create_user(username)
    
    db.users.update_one(user, {"$set": add_dict})
    return make_profile_dao(get_user(username))


def delete_user(username):
    """Delete the specified user"""
    db = client.Cluster0
    db.users.delete_many({"username": username})
    return True


def drop_users():
    """Delete all users"""
    db = client.Cluster0
    db.users.drop()
    return True