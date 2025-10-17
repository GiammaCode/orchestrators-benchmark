from flask import Blueprint, request, jsonify
from app.services import assignment_service

assignments_bp = Blueprint('assignments', __name__)


@assignments_bp.route('/assignments', methods=['POST'])
def create_assignment():
    """
    Create a new assignment.
    """
    # TODO: Aggiungere un decoratore per il controllo dell'autenticazione admin
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        assignment_id = assignment_service.create_assignment(data)
        return jsonify({
            "assignment_id": assignment_id,
            "message": "Assignment created successfully"
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@assignments_bp.route('/assignments/active', methods=['GET'])
def get_active_assignments():
    """
    Return a list of all active assignments.
    """
    active_assignments = assignment_service.get_active_assignments()
    return jsonify(active_assignments), 200


@assignments_bp.route('/assignments/<assignment_id>', methods=['GET'])
def get_assignment(assignment_id):
    """
    Return details of a specific assignment.
    """
    assignment = assignment_service.get_assignment_details(assignment_id)

    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    return jsonify(assignment), 200