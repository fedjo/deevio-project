import json

from flask import Blueprint
from flask import jsonify

from predictionsapp.db import get_db

bp = Blueprint('api', __name__)
# mongoc = MongoClient("mongodb://mongodb:27017") #host uri
# db = mongoc.mymongodb    #Select the database


@bp.route('/', methods=['GET'])
def index():
    print("sad")
    return "Hello deevio"


@bp.route('/api/v1/prediction/<int:pred_id>', methods=['GET'])
def get_predictions(pred_id):
    db = get_db()
    predictions = [{"pred": "nail"}]
    return jsonify(predictions)


@bp.route('/api/v1/weakpredictions/', methods=['GET'])
def get_weak_prediction():
    weak_predictions = [{"imid": "111"}]
    return jsonify(weak_predictions)


