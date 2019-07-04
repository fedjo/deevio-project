from flask import Flask


def create_app(app_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if app_config is None:
        app.config.from_pyfile('config.py', silent=True)
        app.logger.info(app.config)
    else:
        app.config.update(app_config)

    # Register command to flush database
    from predictionsapp import db
    db.init_db_command_register(app)

    # Ensure Indexes
    # with app.app_context():
    #    db.create_index('classification', 'imageId')

    # Register blueprint for the Rest api
    from predictionsapp import api
    app.register_blueprint(api.bp)

    # Init mqtt backend
    app.logger.info("Connecting to MQTT")
    from predictionsapp.mqtt import MQTT
    MQTT(app)

    return app
