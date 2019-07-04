MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DBNAME = 'data-classification'

MQTT_BROKER = 'mqtt'
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

classification_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string"},
        "imagePath": {"type": "string"},
        "imageId": {"type": "string"},
        "output": {
            "type": "object",
            "properties": {
                "probability": {"type": "number"},
                "label": {"type": "string"},
                "result": {"type": "string"},
                "bbox": {"type": "array"}
            }
        }
    }
}
