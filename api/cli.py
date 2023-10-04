from . import model
from .app import app

import click


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
