from os import environ as env
from operator import itemgetter

import click

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .app import app

uri = f'mongodb+srv://{env.get("mongo_atlas_username")}:{env.get("mongo_atlas_passwd")}@cluster0.th5fhnb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


@app.cli.command("ping")
def _():
    """Send a ping to the database to confirm a connection"""
    return ping()

def ping():
    """Send a ping to the database to confirm a connection"""
    try:
        client.admin.command('ping')
        click.echo("Pinged your deployment. You successfully connected to MongoDB!")
        return True
    except Exception as e:
        click.echo(e)
        return False


def make_user_dao(user_raw):
    """Create a DAO"""
    if user_raw is None:
        return {}
    return itemgetter("username")(user_raw)


@app.cli.command("get-user")
@click.argument("username")
def _(username):
    """Get a user"""
    return get_user(username)


def get_user(username):
    """Get a user"""
    db = client.Cluster0
    user = db.users.find_one({"username": username})
    click.echo(f"Found user {user}")
    user = make_user_dao(user)
    return user



@app.cli.command("create-user")
@click.argument("username")
def _(username):
    """Create a new user"""
    return create_user(username)


def create_user(username):
    """Create a new user"""
    db = client.Cluster0
    db.users.insert_one({"username": username})
    click.echo(f"Created user {username}")