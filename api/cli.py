from . import model
from .app import app

import click, json


@app.cli.command("ping")
def _():
    """Send a ping to the database to confirm a connection"""
    if model.ping():
        click.echo("Connected to database")
    else:
        click.echo("Could not connect to database")


@app.cli.command("get-user")
@click.argument("username")
def _(username):
    """Get a user"""
    click.echo(model.get_user(username))


@app.cli.command("create-user")
@click.argument("username")
def _(username):
    """Create a new user"""
    model.get_or_create_user(username)
    click.echo(f"Created user {username}")


@app.cli.command("update-user")
@click.argument("username")
@click.argument("add_dict")
def _(username, add_dict):
    """Add a new field to the user"""
    add_dict = json.loads(add_dict)
    model.add_fields(username, add_dict)
    click.echo(f"Added {add_dict} to {username}")


@app.cli.command("delete-user")
@click.argument("username")
def _(username):
    """Delete a user"""
    model.delete_user(username)
    click.echo(f"Deleted user {username}")


@app.cli.command("load-users")
@click.argument("filename")
def _(filename):
    """Load users from a file"""
    with open(filename) as f:
        users = json.load(f)
    for user in users:
        model.get_or_create_user(user)
    click.echo(f"Loaded {len(users)} users from {filename}")


@app.cli.command("clobber-users")
@click.argument("filename")
def _(filename):
    """Replace all users with the users in a file"""
    model.drop_users()
    users=[]
    with open(filename) as f:
        users = json.loads(f.read())
    for user in users:
        model.create_user(user)
    click.echo(f"Dropped db and added {len(users)} users from {filename}")