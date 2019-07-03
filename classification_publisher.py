import json

import paho.mqtt.client as mqtt


prediction = {
        "status":"complete",
        "imagePath":"20180907/1536311270718.jpg",
        "imageId":"1536311270718",
        "output":[
            {
                "bbox":[
                    1008.8831787109375,
                    280.6226501464844,
                    1110.0245361328125,
                    380.72021484375

                    ],
                "probability":0.9725130796432495,
                "label":"nail",
                "result":"good"
                }
            ]
        }

def on_connect(client, userdata, flags, rc):
    current_app.logger.info("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("new_prediction")


def on_subscribe(client, userdata, mid, granted_qos):
    current_app.logger.info("Successfully subscribed with mid " + str(mid))


def on_message(client, userdata, msg):
    current_app.logger.info(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.on_message = on_message
    mqttc.connect("127.0.0.1", 1883)
    mqttc.loop_start()

    while True:
        predictionstr = json.dumps(prediction)
        mqttc.publish("new_prediction", predictionstr)
