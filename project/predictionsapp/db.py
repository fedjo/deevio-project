from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

import click
from flask import current_app, g
from flask.cli import with_appcontext


# Create a mongodb client
# Use the same client across request context
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

    return g.dbc


# Get the database
def get_db():
    return get_client()[current_app.config['MONGO_DBNAME']]


# Create collection index for specified key
def create_index(col, key):
    db = get_db()
    try:
        db[col].create_index(key)
    except Exception as e:
        current_app.logger.error(str(e))
    current_app.logger.info("Created index for collection {} and key {}"
                            .format(col, key))


# Ensure indexes
def ensure_indexes(app):
    with app.app_context():
        create_index("classification", "imageId")


#  Update an existing classification result
def update_classification(doc):
    db = get_db()
    current_app.logger.debug("Updating document to database")
    q = {"imageId": str(doc['imageId'])}
    update_op = {"$set": {},
                 "$push": {}
                 }
    for k in doc:
        if type(doc[k]) is not list:
            update_op['$set'][k] = doc[k]
        else:
            update_op['$push'][k] = {"$each": doc[k]}
    current_app.logger.debug(update_op)
    try:
        res = db.classification.update_one(q, update_op, True)
    except OperationFailure as e:
        current_app.logger.debug(str(e))
        raise
    except Exception as ex:
        raise
        current_app.logger.debug(str(ex))
    if not res.upserted_id:
        return res.modified_count
    return res.upserted_id


# Insert a classification to collection db
def insert_classification(doc):
    db = get_db()
    current_app.logger.debug("Adding document to database")
    try:
        res = db.classification.insert_one(doc)
    except OperationFailure as e:
        current_app.logger.debug(str(e))
        raise
    except Exception as ex:
        current_app.logger.debug(str(ex))
        raise
    return res.inserted_id


# Remove a classification from collection db
def remove_classification_by_id(oid):
    db = get_db()
    current_app.logger.debug("Deleting document from database")
    q = {"_id": oid}
    try:
        res = db.classification.delete_one(q)
    except Exception as e:
        current_app.logger.debug(str(e))
        raise
    return res.deleted_count


# Remove a classification from collection db
def remove_classification_by_imgid(imgid):
    db = get_db()
    current_app.logger.debug("Deleting document from database")
    q = {"imageId": str(imgid)}
    try:
        res = db.classification.delete_one(q)
    except Exception as e:
        current_app.logger.debug(str(e))
        raise
    return res.deleted_count


# Get image predictions
def get_img_predictions(imgid, skip, limit):
    db = get_db()
    # Query created
    q = {"imageId": str(imgid)}
    # Return just the output array
    # Do not return _id which not serializable
    projection = {"_id": False, "output": True}
    current_app.logger.debug("Excecuting query: {} with projection: {}"
                             .format(str(q), str(projection)))
    try:
        cursor = (db.classification.find(q, projection)
                  .skip(skip).limit(limit)
                  )
    except OperationFailure as e:
        current_app.logger.debug(str(e))
        raise
    except Exception as ex:
        current_app.logger.debug(str(ex))
        raise
    return list(cursor)


# Get weak classifications according to boundary
def get_weak_classifications(prob_boundary, skip, limit):
    db = get_db()
    # Query created
    q = {"output.probability": {"$lte": prob_boundary}}
    # Do not return _id which not serializable
    projection = {"_id": False}
    current_app.logger.debug("Excecuting query: {} with projection: {}"
                             .format(str(q), str(projection)))
    try:
        cursor = (db.classification.find(q, projection)
                  .skip(skip).limit(limit)
                  )
    except OperationFailure as e:
        current_app.logger.debug(str(e))
        raise
    except Exception as ex:
        current_app.logger.debug(str(ex))
        raise
    return list(cursor)


# Close the database connection
def close_client(e=None):
    # Remove db client from context and close db
    dbc = g.pop('dbc', None)
    if dbc is not None:
        dbc.close()


# Initialize the database
def init_db():
    dbc = get_client()
    dbc.drop_database(current_app.config['MONGO_DBNAME'])


# CLI command to initialize the database
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized database')


# Register CLI command
def init_db_command_register(app):
    app.teardown_appcontext(close_client)
    app.teardown_request(close_client)
    app.cli.add_command(init_db_command)
