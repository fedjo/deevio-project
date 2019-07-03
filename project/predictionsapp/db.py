from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():

    if 'db' not in g:
        g.db = MongoClient(
            current_app.config['MONGO_HOST'],
            current_app.config['MONGO_PORT']
        )
        try:
            # The ismaster command is cheap and does not require auth.
            g.db.admin.command('ismaster')
        except ConnectionFailure:
            current_app.logger.error("Server not available")
        current_app.logger.info("Database connection established!")

    return g.db.current_app.config['MONGO_DBNAME']


def close_db(e=None):

    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():

    db = get_db()
    db.drop_database(current_app.config['MONGO_DBNAME'])


@click.command('init-db')
@with_appcontext
def init_db_command():

    init_db()
    click.echo('Initialized database')


def init_db_command_register(app):

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
