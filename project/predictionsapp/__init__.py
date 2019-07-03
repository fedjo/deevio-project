import os

from flask import Flask


def create_app(app_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if app_config is None:
        app.config.from_pyfile('config.py', silent=True)
        app.logger.info(app.config)
    else:
        app.config.update(app_config)

    # register the database commands
    from predictionsapp import db
    db.init_db_command_register(app)

    # apply the blueprints to the app
    from predictionsapp import api
    app.register_blueprint(api.bp)

    # Init mqtt subscription
    app.logger.info("Connecting to MQTT")
    # from predictionsapp import mqtt
    # mqtt.init_mqtt(app)

    return app
