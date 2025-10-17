import hashlib
from datetime import datetime
from bson.objectid import ObjectId
from ..extensions import mongo
from ..config import Config

def create_submission(student_id, assignment_id, course_id, file):
    """
     Service layer: manages the business logic for creating a submission.
    """
    if not all([student_id, assignment_id, course_id, file]):
        raise ValueError("Missing required parameters")

    file_content = file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()

    #to save file
    file_path = Config.UPLOAD_DIR / course_id / assignment_id / student_id
    file_path.mkdir(parents=True, exist_ok=True)
    file_full_path = file_path / file.filename

    with open(file_full_path, 'wb') as file:
        file.write(file_content)

    #DB datas to be inserted
    submission_data = {
        "student_id": student_id,
        "assignment_id": assignment_id,
        "course_id": course_id,
        "file_path": str(file_full_path),
        "file_hash": file_hash,
        "file_size": len(file_content),
        "timestamp": datetime.utcnow(),
        "status": "pending"
    }
    result = mongo.db.submissions.insert_one(submission_data)

    return {
        "submission_id": str(result.inserted_id),
        "timestamp": submission_data["timestamp"].isoformat(),
        "status": "pending",
        "file_hash": file_hash
    }

def get_submission_by_student(student_id):
    """ Retrieve all submissions for a student."""
    submissions = list(mongo.db.submissions.find(
        {"student_id": student_id},
        {"_id": 1, "assignment_id": 1, "course_id": 1, "timestamp": 1, "status": 1, "file_size": 1}
    ).sort("timestamp", -1))

    for sub in submissions:
        sub["submission_id"] = str(sub.pop("_id"))
        sub["timestamp"] = sub["timestamp"].isoformat()
    return submissions


def get_submission_file(submission_id):
    """ Retrieve a path of a specific submission"""
    submission = mongo.db.submissions.find_one({"_id": ObjectId(submission_id)})
    if not submission:
        return None
    return submission["file_path"]