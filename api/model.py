from os import environ as env

import click

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .app import app

uri = f'mongodb+srv://{env.get("mongo_atlas_username")}:{env.get("mongo_atlas_passwd")}@cluster0.th5fhnb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.cli.command("get-user")
@click.argument("username")
def get_user(username):
    """Get a user"""
    db = client.Cluster0
    user = db.users.find_one({"username": username})
    print(f"Found user {user}")


@app.cli.command("create-user")
@click.argument("username")
def create_user(username):
    """Create a new user"""
    db = client.Cluster0
    db.users.insert_one({"username": username})
    print(f"Created user {username}")