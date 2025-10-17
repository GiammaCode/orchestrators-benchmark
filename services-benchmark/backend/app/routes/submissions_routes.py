from flask import Blueprint, request, jsonify, send_file
import time
from app.services import submission_service
from config import Config

submissions_bp = Blueprint('submissions', __name__)

@submissions_bp.route('/submit', methods=['POST'])
def submit():
    time.sleep(Config.PROCESSING_DELAY)

    try:
        student_id = request.form.get('student_id')
        assigment_id = request.form.get('assigment_id')
        course_id = request.form.get('course_id')
        file = request.files.get('file')

        result = submission_service.create_submission(student_id, assigment_id, course_id, file)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@submissions_bp.route('/submissions/<student_id>', methods=['GET'])
def get_submission(student_id):
    submissions= submission_service.get_submission_by_student(student_id)
    return jsonify(submissions), 200

@submissions_bp.route('/download/<submission_id>', methods=['GET'])
def download_submission(submission_id):
    file_path = submission_service.get_submission_file(submission_id)
    if not file_path:
        return jsonify({"error": "Submission not found"}), 404

    return send_file(file_path, as_attachment=True)
