import datetime
from flask import Blueprint, request, Response, jsonify
from ..services import mongodb
from ..utils import json_encoder


assignments_bp = Blueprint('assignments_bp', __name__, url_prefix='/assignments')

@assignments_bp.route('', methods=['POST'])
def create_assignment():
    """
    Creates a new assignment - professor side
    """

    if mongodb.assignments_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    try:
        data = request.json
        if not data or 'title' not in data:
            return jsonify({"error": "Title missing"}), 400

        new_assignment = {
            "title": data.get('title'),
            "description": data.get('description', ''),
            "due_date": data.get('due_date'),  # Assumiamo formato ISO
            "created_at": datetime.datetime.now(datetime.timezone.utc)
        }

        result = mongodb.assignments_collection.insert_one(new_assignment)

        # Retrieve the document to return it
        created_doc = mongodb.assignments_collection.find_one({"_id": result.inserted_id})
        return Response(json_encoder.bson_to_json(created_doc), mimetype='application/json'), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@assignments_bp.route('', methods=['GET'])
def get_all_assignments():
    """
    Retrieves all existing assignments - professor & student side
    :return:
    """
    if mongodb.assignments_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    try:
        assignments = list(mongodb.assignments_collection.find({}))
        return Response(json_encoder.bson_to_json(assignments), mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
