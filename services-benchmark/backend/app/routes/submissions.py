import datetime
from flask import Blueprint, request, Response, jsonify
from ..services import mongodb
from ..utils import json_encoder

submissions_bp = Blueprint('submissions_bp', __name__, url_prefix='/submissions')

@submissions_bp.route('', methods=['POST'])
def create_submission():
    """
    Create a new submission - student side
    """
    return "POST submission"


@submissions_bp.route('', methods=['GET'])
def get_all_submissions():
    """
    Retrieve all submissions - professor side
    """
    return "GET all submissions"

@submissions_bp.route('/{submissionId}', methods=['GET'])
def get_submission(submissionId):
    """
    Retrieve details of a specific submission
    """
    return {"submissionId": submissionId}
