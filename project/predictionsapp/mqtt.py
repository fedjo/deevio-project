import json

import paho.mqtt.client as mqttc


class MQTT():
    """Main MQTT class"""

    def __init__(self, app=None):
        self.app = app
        self.connected = False
        self.client = mqttc.Client()

        if app is not None:
            self.init_params(app)

    def init_params(self, app):
        # Get configuration from app config
        self.broker_url = app.config['MQTT_BROKER']
        self.broker_port = app.config['MQTT_PORT']
        self.broker_keepalive = app.config['MQTT_KEEPALIVE']

        # Set the callbacks
        self.client.on_connect = self._on_connect
        self.client.on_subscribe = self._on_subscribe
        self.client.on_message = self._on_message

        # Connecting
        self.client.loop_start()
        app.logger.info("Started mqtt looping")

        rc = self.client.connect(
            self.broker_url,
            self.broker_port,
            self.broker_keepalive
        )

        if rc == 0:
            app.logger.info("MQTT broker connected!")
        else:
            app.logger.error("Could not connect to MQTT Broker, \
                             Error Code: {0}".format(rc))

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client, userdata, flags, rc):
        self.app.logger.info("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("new_prediction")

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        self.app.logger.info("Successfully subscribed with mid " + str(mid))

    def _on_message(self, client, userdata, msg):
        self.app.logger.info(msg.topic + " " + str(msg.payload))