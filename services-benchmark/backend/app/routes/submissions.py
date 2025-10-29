import datetime
from flask import Blueprint, request, Response, jsonify
from ..services import mongodb
from ..utils import json_encoder
from bson import ObjectId

submissions_bp = Blueprint('submissions_bp', __name__, url_prefix='/submissions')

@submissions_bp.route('', methods=['GET'])
def get_all_submissions():
    """
    Retrieve all submissions - professor side
    """
    if mongodb.submissions_collection is None:
        return jsonify({"error": "Database not connected"}), 500
    try:
        submissions = list(mongodb.submissions_collection.find())
        return Response(json_encoder.bson_to_json(submissions), mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@submissions_bp.route('/{submissionId}', methods=['GET'])
def get_submission(submission_id):
    """
    Retrieve details of a specific submission
    """
    if mongodb.submissions_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    try:
        if not ObjectId.is_valid(submission_id):
            return jsonify({"error": "submission ID not valid"}), 400

        submission = mongodb.submissions_collection.find_one({"_id": ObjectId(submission_id)})

        if not submission:
            return jsonify({"error": "Submission not found"}), 404

        return Response(json_encoder.bson_to_json(submission), mimetype='application/json')

    except Exception as e:
        return jsonify({"error": str(e)}), 500
