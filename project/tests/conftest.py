import pytest

from predictionsapp import create_app
from predictionsapp import db


MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DBNAME = 'classification-data-test'

MQTT_BROKER = 'mqtt'
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'MONGO_HOST': MONGO_HOST,
        'MONGO_PORT': MONGO_PORT,
        'MONGO_DBNAME': MONGO_DBNAME,
        'MQTT_BROKER': MQTT_BROKER,
        'MQTT_PORT': MQTT_PORT,
        'MQTT_KEEPALIVE': MQTT_KEEPALIVE
    })

    with app.app_context():
        db.init_db()

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    client = app.test_client()
    return client
