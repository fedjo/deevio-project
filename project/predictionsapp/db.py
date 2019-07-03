from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_client():

    if 'dbc' not in g:
        g.dbc = MongoClient(
            current_app.config['MONGO_HOST'],
            current_app.config['MONGO_PORT']
        )
        try:
            # The ismaster command is cheap and does not require auth.
            g.dbc.admin.command('ismaster')
        except ConnectionFailure:
            current_app.logger.error("Server not available")
        current_app.logger.info("Database connection established!")

    current_app.logger.info(g)
    return g.dbc


def get_db():
    return get_client()[current_app.config['MONGO_DBNAME']]


def get_predictions_by_imgid(imgid, skip, limit):
    db = get_db()
    q = {"imageId": str(imgid)}
    projection = {"_id": False, "output": True}
    current_app.logger.debug("Excecuting query: {} with projection: {}"
                             .format(str(q), str(projection)))
    pred_cursor = db.predictions.find(q, projection).skip(skip).limit(limit)
    return list(pred_cursor)


def get_weak_classifications(prob_boundary, skip, limit):
    db = get_db()
    q = {"output.probability": {"$lte": prob_boundary}}
    projection = {"_id": False}
    current_app.logger.debug("Excecuting query: {} with projection: {}"
                             .format(str(q), str(projection)))
    weak_classifications = db.predictions.find(q, projection).skip(skip).limit(limit)
    return list(weak_classifications)


def close_client(e=None):

    dbc = g.pop('dbc', None)

    if dbc is not None:
        dbc.close()


def init_db():

    dbc = get_client()
    dbc.drop_database(current_app.config['MONGO_DBNAME'])


@click.command('init-db')
@with_appcontext
def init_db_command():

    init_db()
    click.echo('Initialized database')


def init_db_command_register(app):

    app.teardown_appcontext(close_client)
    app.cli.add_command(init_db_command)
