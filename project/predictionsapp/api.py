from flask import (current_app, Blueprint, request,
                   jsonify, make_response, abort)

from predictionsapp import db


bp = Blueprint('api', __name__)


# Index call
@bp.route('/', methods=['GET'])
def index():
    return "Hello deevio"


# Get predictions of the specified image
@bp.route('/api/v1/predictions/<int:imgid>', methods=['GET'])
def get_predictions(imgid):

    # Get pagination values as request params
    skip = int(request.args['skip']) if 'skip' in request.args else 0
    limit = int(request.args['limit']) if 'limit' in request.args else 0
    current_app.logger.debug("Skip: {} Limit: {}"
                             .format(str(skip), str(limit)))

    # Query db for the specified image
    predictions = db.get_img_predictions(imgid, skip, limit)
    # If an error occured raise 500 error
    if predictions is None:
        abort(500)
    # If imageId does not exist in database raise 404 not found
    if len(predictions) == 0:
        abort(404)
    return make_response(jsonify(predictions), 200)


# Get all weak classifications
@bp.route('/api/v1/classifications/weak', methods=['GET'])
def get_weak_classifications():

    # Get weak boundary as request param or set to default value 0.7
    boundary = request.args['boundary'] if 'boundary' in request.args else 0.7

    # Get pagination values as request params or set default values to 0
    skip = int(request.args['skip']) if 'skip' in request.args else 0
    limit = int(request.args['limit']) if 'limit' in request.args else 0
    current_app.logger.debug("Skip: {}, Limit: {} Boud: {}"
                             .format(str(skip), str(limit), str(boundary)))

    # Query db for weak classifications
    weak_classifications = db.get_weak_classifications(boundary, skip, limit)
    # If an error occured raise 500 error
    if weak_classifications is None:
        abort(500)
    return make_response(jsonify(weak_classifications), 200)
