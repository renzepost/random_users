#!/usr/bin/env python
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from random_users import DB_URI
from random_users.operations import (
    dump_to_csv,
    get_user_data_api,
    insert_user_data,
    query_users,
)

engine = create_engine(DB_URI)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()


@click.group()
def cli():
    pass


@cli.command()
def import_users():
    data = get_user_data_api()
    insert_user_data(session, data)


@cli.command()
def export_users():
    dump_to_csv(session, "export.csv")


@cli.command()
@click.argument("filters", nargs=-1)
def show_users(filters):
    filters = [tuple(filter.split("=")) for filter in filters]
    result = query_users(session, filters)
    print(result)


def main():
    cli()


if __name__ == "__main__":
    main()
