from flask import current_app, Blueprint, request, jsonify

from predictionsapp.db import (get_predictions_by_imgid,
                               get_weak_classifications)

bp = Blueprint('api', __name__)
# mongoc = MongoClient("mongodb://mongodb:27017") #host uri
# db = mongoc.mymongodb    #Select the database


@bp.route('/', methods=['GET'])
def index():
    print("sad")
    return "Hello deevio"


@bp.route('/api/v1/prediction/<int:imgid>', methods=['GET'])
def get_predictions(imgid):
    skip = int(request.args['skip']) if 'skip' in request.args else 0
    limit = int(request.args['limit']) if 'limit' in request.args else 0
    current_app.logger.info("Skip: {}, Limit: {}".format(str(skip), str(limit)))
    predictions = get_predictions_by_imgid(imgid, skip, limit)
    return jsonify(predictions)


@bp.route('/api/v1/weakpredictions/', methods=['GET'])
def get_weak_prediction():
    boundary = request.args['boundary'] if 'boundary' in request.args else 0.7
    skip = int(request.args['skip']) if 'skip' in request.args else 0
    limit = int(request.args['limit']) if 'limit' in request.args else 0
    current_app.logger.info("Skip: {}, Limit: {} Boud: {}".format(str(skip), str(limit), str(boundary)))
    weak_classifications = get_weak_classifications(boundary, skip, limit)
    return jsonify(weak_classifications)
