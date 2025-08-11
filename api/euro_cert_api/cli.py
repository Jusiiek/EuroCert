import click
import asyncio
from functools import wraps

from euro_cert_api.utils.fixtures import load_users
from euro_cert_api.db import init_db


def coroutine(f):
    """takes an asynchronous function f as input."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    """This is a management script for euro cert api."""


@cli.command()
@coroutine
async def load_fixtures():
    await init_db()
    await load_users()


if __name__ == "__main__":
    cli()
