import json

from predictionsapp import db


doc = {
    "status": "complete",
    "imagePath": "20180907/1536311270718.jpg",
    "imageId": "1536311270718",
    "output": [
        {
            "bbox": [
                1008.8831787109375,
                280.6226501464844,
                1110.0245361328125,
                380.72021484375
            ],
            "probability": 0.9725130796432495,
            "label": "nail",
            "result": "good"

        }
    ]
}


# Test the index api call
def test_index(client):
    rs = client.get('/')
    assert b'Hello deevio' in rs.data


# Test /api/v1/predictions/<imgid>
def test_get_predictions(app, client):

    with app.app_context():
        db.insert_classification(doc)

    # Check if prediction retrieved correctly
    rs = client.get('/api/v1/predictions/' + doc['imageId'])
    jsonrs = json.loads(rs.data.decode('utf-8', 'ignore'))
    assert jsonrs[0]['output'] == doc['output']

    with app.app_context():
        db.remove_classification_by_imgid(doc['imageId'])

    # Check if not matching imageId
    rs = client.get('/api/v1/predictions/' + doc['imageId'])
    assert rs.status_code == 404


# Test /ap1/v1/classifications/weak/
def test_get_weak_classifications(app, client):
    _doc = dict(doc)
    _doc['output'][0]['probability'] = 0.67

    with app.app_context():
        db.insert_classification(_doc)
    _doc.pop('_id', None)

    # Check if prediction retrieved correctly
    rs = client.get('/api/v1/classifications/weak')
    jsonrs = json.loads(rs.data.decode('utf-8', 'ignore'))
    assert jsonrs[0] == _doc

    with app.app_context():
        db.remove_classification_by_imgid(doc['imageId'])

    # Check if prediction retrieved correctly
    rs = client.get('/api/v1/classifications/weak')
    jsonrs = json.loads(rs.data.decode('utf-8', 'ignore'))
    assert jsonrs == []
