from flask import Blueprint, jsonify
from datetime import datetime
from ..services import monitoring_service

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/monitoring', methods=['GET'])
def health():
    """
    Return health status of the service, check mongodb and volumes
    accessibility.
    """
    status_details = monitoring_service.check_health()
    is_fully_healthy = all(
        status == 'connected' or
        status == 'accessible' for status in status_details.values()
    )

    response = {
        "status": "healthy" if is_fully_healthy else "degraded",
        "components": status_details,
        "timestamp": datetime.utcnow().isoformat()
    }

    status_code = 200 if is_fully_healthy else 503
    return jsonify(response), status_code


@monitoring_bp.route('/stats', methods=['GET'])
def stats():
    """
    Return statistics about the service.

    """
    application_stats = monitoring_service.get_application_stats()
    application_stats["timestamp"] = datetime.utcnow().isoformat()

    return jsonify(application_stats), 200