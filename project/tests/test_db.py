
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


def test_insert_remove_classification(app):
    with app.app_context():
        # Add document to database
        oid = db.insert_classification(doc)
        assert oid is not None

        # Delete from database
        del_count = db.remove_classification_by_id(oid)
        assert del_count == 1
