import sys
import time
import json
import random
import datetime

import paho.mqtt.client as mqtt
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


prediction_tmp = {
    "bbox": [],
    "probability": 0.9725130796432495,
    "label": "nail",
    "result": "good"
}

classification_result_tmp = {
    "status": "complete",
    "imagePath": "20180907/1536311270718.jpg",
    "imageId": "1536311270718",
    "output": []
}


# Create a prediction object based on the template
def prediction():

    prediction = dict(prediction_tmp)
    # Select random numberus that help create equally weighted predicitons
    i = random.randint(0, 1)
    j = random.randint(0, 2)
    weak_boundary = 0.7
    labels = ['nail', 'scratch', 'break']
    label = labels[j]
    if i == 0:
        probability = random.uniform(0.1, weak_boundary)
    else:
        probability = random.uniform(weak_boundary + 0.01, 0.99)

    # Min, max of width, height (randomly selected)
    width = random.uniform(20.0, 500.0)
    height = random.uniform(20.0, 500.0)

    # Select bbox upper-left point
    x_point = random.uniform(0.0, 1500.0)
    y_point = random.uniform(0.0, 1500.0)

    prediction['probability'] = probability
    prediction['label'] = label
    bbox = [x_point, y_point, width, height]
    prediction['bbox'] = bbox
    return prediction


# Create a classification object based on the template
def classification_result():

    classification_result = dict(classification_result_tmp)
    # Select to random number that help populate random classification result
    i = random.randint(1, 9999)
    j = random.randint(1, 9999)

    # Set status according to i's eveneen/oddness
    status = "processing"
    if (i % 2) == 0:
        status = "complete"

    # Construct imageId, imagePath
    imageId = str(i * j)
    imagePath = '{:%Y%m%d}'.format(datetime.date.today()) + '/' + imageId

    # Define the number of prediction
    predno = (i % 3) + 1
    pred_list = list()
    for p in range(1, predno):
        pred_list.append(prediction())
    classification_result['output'] = pred_list

    classification_result['status'] = status
    classification_result['imagePath'] = imagePath
    classification_result['imageId'] = imageId

    return classification_result


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("new_prediction")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Successfully subscribed with mid " + str(mid))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":

    action = sys.argv[1]

    if action == 'pubmqtt':
        print("Publishing results to MQTT bus...")
        mqttc = mqtt.Client()
        mqttc.on_connect = on_connect
        mqttc.on_subscribe = on_subscribe
        mqttc.on_message = on_message
        mqttc.connect("mqtt", 1883)
        mqttc.loop_start()

        while True:
            classificationstr = json.dumps(classification_result())
            mqttc.publish("new_prediction", classificationstr)
            time.sleep(15)
    elif action == 'warmdb':
        print("Populating database...")
        dbc = MongoClient(
            'mongodb',
            27017
        )
        try:
            # The ismaster command is cheap and does not require auth.
            dbc.admin.command('ismaster')
        except ConnectionFailure:
            print("Server not available")
        print("Database connection established!")
        db = dbc['data-classification']

        for i in range(1, 150):
            res = db.classification.insert(classification_result())
            print("Added object with _id: " + str(res))
    else:
        print("This action is not yet specified!")
        sys.exit(-1)
